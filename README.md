# 🧠 LeadMind

> Automate lead engagement with AI — intent detection, smart replies, and CRM sync powered by Claude.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## What is LeadMind?

LeadMind is an AI-powered lead engagement platform that uses Large Language Models (LLMs) to automate personalized outreach across email and SMS. It analyzes incoming messages, detects customer intent, generates context-aware replies, and syncs everything with your CRM — reducing manual follow-ups and streamlining your sales pipeline.

---

## Features

- **Intent Detection** — Classifies incoming lead messages into actionable intents (meeting request, pricing question, objection, unsubscribe, and more) using Claude AI
- **Auto-Reply Generation** — Generates personalized, context-aware replies tailored to each lead and their detected intent
- **Smart Routing** — Routes each intent to the right action: book a meeting, send info, handle objections, or flag for human review
- **REST API** — FastAPI-powered endpoint to plug into any messaging pipeline
- **Email & SMS Outreach** — Sends personalized cold outreach via SendGrid and Twilio
- **Bulk Outreach** — Batch process a CSV of leads and generate personalized messages at scale
- **CRM Integration** — Syncs lead interactions with HubSpot automatically (create contacts, log notes, update lifecycle stages)
- **Calendly Scheduling** — Automates meeting booking directly from detected meeting-request intents
- **Lead Dashboard** — React + Tailwind frontend to monitor leads, intents, urgency, and pipeline stages

---

## Project Structure

```
leadmind/
├── phase1-intent-detection/
│   ├── classifier.py          # Intent classification via Claude API
│   ├── reply_generator.py     # Context-aware reply generation
│   ├── router.py              # Intent routing + full pipeline
│   ├── api.py                 # FastAPI endpoint
│   └── test_messages.py       # Pytest test suite
├── phase2-outreach/
│   ├── outreach_generator.py  # Cold email, SMS, and follow-up generator
│   └── bulk_outreach.py       # Batch process a CSV of leads
├── phase3-integrations/
│   ├── send_email.py          # SendGrid email sender
│   ├── send_sms.py            # Twilio SMS sender
│   ├── calendly.py            # Fetch event types + scheduling links
│   ├── crm.py                 # HubSpot contact management
│   └── pipeline.py            # Full end-to-end workflow
├── phase4-dashboard/
│   ├── src/
│   │   ├── App.jsx            # Main dashboard component
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)
- A [Twilio account](https://www.twilio.com/) — for SMS
- A [SendGrid account](https://sendgrid.com/) — for email
- A [HubSpot account](https://www.hubspot.com/) — for CRM
- A [Calendly account](https://calendly.com/) — for scheduling

> For Phase 1 only, you just need the Anthropic API key. Add the rest when you're ready for Phases 2–3.

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/leadmind.git
cd leadmind

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in your keys
```

### Run the API (Phase 1)

```bash
cd phase1-intent-detection
uvicorn api:app --reload
```

API will be live at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run the Dashboard (Phase 4)

```bash
cd phase4-dashboard
npm install
npm run dev
```

Dashboard will be live at `http://localhost:3000`.

---

## Usage

### Process a lead message

```bash
curl -X POST http://localhost:8000/process-message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Id love to see a demo — when are you free?",
    "lead_name": "Sarah",
    "lead_company": "Acme Logistics",
    "rep_name": "Alex",
    "company_context": "AI-powered route optimization for logistics teams"
  }'
```

### Example response

```json
{
  "intent": "meeting_request",
  "confidence": 0.97,
  "sentiment": "positive",
  "urgency": "medium",
  "action": "schedule_meeting",
  "key_signals": ["love to see a demo", "when are you free"],
  "reply": "Hi Sarah, great to hear from you! Id love to show you what we've built for logistics teams like Acme. Here's my calendar to grab a 30-min slot that works for you: [CALENDLY_LINK]. Looking forward to connecting!\n\nBest,\nAlex"
}
```

### Supported intents

| Intent | Action |
|---|---|
| `meeting_request` | Books a Calendly meeting |
| `pricing_question` | Sends pricing info + invites to call |
| `objection` | Handles concern + keeps conversation going |
| `positive_interest` | Nurtures lead with next step |
| `unsubscribe` | Stops outreach + logs in CRM |
| `out_of_office` | Schedules a follow-up |
| `unknown` | Flags for human review |

### Run bulk outreach from a CSV

```bash
cd phase2-outreach
python bulk_outreach.py
```

Expected CSV format (`leads.csv`):

```
name,company,role,industry,pain_point,channel
Sarah,Acme Logistics,Head of Operations,Logistics,Manual route planning,email
James,TechFlow,VP Sales,SaaS,Low reply rates,sms
```

### Run the full end-to-end pipeline

```bash
cd phase3-integrations
python pipeline.py
```

This will classify the message, generate a reply, send it via email or SMS, log it to HubSpot, and update the lead's lifecycle stage — all automatically.

---

## Running Tests

```bash
cd phase1-intent-detection
pytest test_messages.py -v
```

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# ── Phase 1 ──────────────────────────────
ANTHROPIC_API_KEY=your_key_here

# ── Phase 3 ──────────────────────────────
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=

HUBSPOT_API_KEY=
CALENDLY_API_KEY=
CALENDLY_USER_URI=
```

---

## Roadmap

- [x] Phase 1 — Intent detection & auto-reply system
- [x] Phase 2 — Personalized email & SMS outreach generator
- [x] Phase 3 — CRM, Twilio, SendGrid & Calendly integrations
- [x] Phase 4 — React lead management dashboard

---

## Tech Stack

- **[Claude API](https://docs.anthropic.com/)** — LLM for intent classification and reply generation
- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API framework
- **[Twilio](https://www.twilio.com/)** — SMS delivery
- **[SendGrid](https://sendgrid.com/)** — Email delivery
- **[HubSpot](https://developers.hubspot.com/)** — CRM sync
- **[Calendly](https://developer.calendly.com/)** — Meeting scheduling
- **[React](https://react.dev/) + [Vite](https://vitejs.dev/) + [Tailwind CSS](https://tailwindcss.com/)** — Lead dashboard
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment variable management
- **[Pytest](https://pytest.org/)** — Testing

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

[MIT](./LICENSE)
