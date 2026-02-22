# 🚀 AI Calendar Scheduling Agent

> Natural language → Google Calendar event
> Built with **FastAPI + Groq LLM + Google Calendar API**

---

## ✨ Overview

This project is an **AI-powered scheduling agent** that converts plain text instructions into Google Calendar events.

Example:

```
"Team sync 2026-03-01"
```

➡️ AI extracts data
➡️ Validates date
➡️ Creates Google Calendar event

No manual form filling.
Just text → event.

---

## 🧠 Core Idea

The system combines:

* 🤖 LLM extraction (semantic understanding)
* 🛡️ Deterministic validation (robustness)
* 📅 Google Calendar API (execution)

This hybrid design avoids hallucinations while preserving natural UX.

---

## 🏗️ Architecture

```
┌──────────────┐
│   User Text  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FastAPI    │
│  /schedule   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Groq LLM   │
│ Extraction   │
└──────┬───────┘
       │ JSON
       ▼
┌──────────────┐
│  Validation  │
│  Guardrails  │
└──────┬───────┘
       │ Valid
       ▼
┌──────────────┐
│ Google Auth  │
│ Token Store  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Calendar API │
│ Event Create │
└──────────────┘
```

---

## ⚙️ Tech Stack

### 🔹 Backend

* FastAPI
* Python

### 🔹 AI

* Groq API
* Moonshot Kimi model

### 🔹 Google Integration

* Google OAuth 2.0
* Google Calendar API

### 🔹 Infra

* dotenv secret management
* runtime credential injection

---

## 🔐 Security Design

Sensitive files are never committed.

```
.env
credentials.json
token.json
```

Secrets are injected via environment variables and reconstructed at runtime.

This prevents credential leakage while preserving compatibility with Google SDK.

---

## 🧩 Feature Set

### ✅ Natural language scheduling

Understands simple user intent.

### ✅ Strict date enforcement

Avoids ambiguity and hallucinated scheduling.

### ✅ All-day event support

Uses Calendar date-based events.

### ✅ OAuth token persistence

Avoids repeated authentication.

### ✅ LLM + rule hybrid system

Production-aligned reliability pattern.

---

## 🚀 Setup Guide

### 1️⃣ Clone repo

```
git clone <repo>
cd project
```

### 2️⃣ Install deps

```
pip install -r requirements.txt
```

### 3️⃣ Create `.env`

```
GROQ_API_KEY=xxxx
GOOGLE_CREDS={...json...}
```

### 4️⃣ Run

```
uvicorn main:app --reload
```

---

## 🧪 Example API Call

### Request

```json
POST /schedule

{
  "text": "Doctor visit 2026-03-10"
}
```

### Response

```json
{
  "status": "created",
  "event": {
    "summary": "Doctor visit",
    "date": "2026-03-10"
  }
}
```

---

## 🎯 Design Principles

### 🪶 Minimal user friction

No structured input required.

### 🧠 AI where semantics matter

Extraction handled by LLM.

### 🛡️ Rules where correctness matters

Validation handled by code.

### 🔑 Secrets never in repo

Environment-driven auth.

This pattern mirrors real production agent design.

---

## 🔮 Future Roadmap

* Relative date resolution
* Conversational clarification loop
* Multi-user OAuth web flow
* Recurring event support
* Reminder injection
* Voice scheduling interface
* Agent collaboration layer

---

## 👨‍💻 Author Vision

This project is part of a broader exploration into:

* Agentic infrastructure
* Human-AI collaborative workflows
* Autonomous scheduling assistants
* Multi-agent coordination systems

The goal is not just automation
but **intelligent execution layers**.

---

## ⭐ If you like it

Give a star
Fork it
Build on it

Agents are just getting started.

---
