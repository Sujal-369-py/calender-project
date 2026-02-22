import os
import json
import re
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from groq import Groq

load_dotenv()

app = FastAPI()

# create credentials.json from env if not present

if os.getenv("GOOGLE_CREDS") and not os.path.exists("credentials.json"):
    with open("credentials.json", "w") as f:
        json.dump(json.loads(os.getenv("GOOGLE_CREDS")), f)

#google authentciation

SCOPES = ['https://www.googleapis.com/auth/calendar']

# fetch cresits like client secreate key of goole calender
def get_calendar_service():
    creds = None

    # load token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # login if token missing
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json','w') as token:
            token.write(creds.to_json())

    return build('calendar','v3',credentials=creds)

service = get_calendar_service()

# llm logic is here

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "moonshotai/kimi-k2-instruct-0905"

# for extracting the text and generating the repsonse. (No reestriction or no validation here)
def extract_event(text: str):

    prompt = f"""
Extract meeting info from text.

Return JSON ONLY:
{{
 "summary": "",
 "date": ""
}}

Date must be in YYYY-MM-DD if present.
If missing → null.

Text: {text}
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}]
    )

    raw = res.choices[0].message.content

    json_str = re.search(r'\{.*\}', raw, re.S).group()
    return json.loads(json_str)

# validation if date and summary not specified
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

# validation for summary
def validate(data):

    if not data.get("summary") or not data.get("date"):
        return False

    if not is_valid_date(data["date"]):
        return False

    return True

# backend logic begin here

class MeetingReq(BaseModel):
    text: str

# end point 
@app.post("/schedule")
def schedule_meeting(req: MeetingReq):

    data = extract_event(req.text)

    if not validate(data):
        return {
            "status": "clarify",
            "message": "Give summary + full date in YYYY-MM-DD format."
        }

    # all day event
    event_date = datetime.strptime(data["date"], "%Y-%m-%d")
    end_date = event_date + timedelta(days=1)

    event = {
        'summary': data['summary'],
        'start': {'date': data['date']},
        'end': {'date': end_date.strftime("%Y-%m-%d")},
    }
    # for insertion inside clanender
    service.events().insert(calendarId='primary', body=event).execute()
    # return body
    return {"status":"created","event":data}