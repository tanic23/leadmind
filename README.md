# 🧠 LeadMind

> Automate lead engagement with AI — intent detection, smart replies, and CRM sync powered by Claude.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square)
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
- **CRM Integration** *(Phase 3)* — Syncs lead interactions with HubSpot / Airtable automatically
- **Email & SMS Outreach** *(Phase 2)* — Sends personalized cold outreach via SendGrid and Twilio
- **Calendly Scheduling** *(Phase 3)* — Automates meeting booking directly from detected meeting-request intents
- **Lead Dashboard** *(Phase 4)* — React frontend to monitor leads, intents, and pipeline stages

---

## Project Structure

```
leadmind/
├── phase1-intent-detection/
│   ├── classifier.py        # Intent classification via Claude API
│   ├── reply_generator.py   # Context-aware reply generation
│   ├── router.py            # Intent routing + full pipeline
│   ├── api.py               # FastAPI endpoint
│   └── test_messages.py     # Pytest test suite
├── phase2-outreach/         # Email & SMS outreach generator (coming soon)
├── phase3-integrations/     # CRM, Twilio, SendGrid, Calendly (coming soon)
├── phase4-dashboard/        # React lead dashboard (coming soon)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

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
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the API

```bash
cd phase1-intent-detection
uvicorn api:app --reload
```

The API will be live at `http://localhost:8000`.

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
ANTHROPIC_API_KEY=your_key_here

# Phase 3 — add when ready
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
SENDGRID_API_KEY=
HUBSPOT_API_KEY=
CALENDLY_API_KEY=
```

---

## Roadmap

- [x] Phase 1 — Intent detection & auto-reply system
- [ ] Phase 2 — Personalized email & SMS outreach generator
- [ ] Phase 3 — CRM, Twilio, SendGrid & Calendly integrations
- [ ] Phase 4 — React lead management dashboard

---

## Tech Stack

- **[Claude API](https://docs.anthropic.com/)** — LLM for intent classification and reply generation
- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API framework
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment variable management
- **[Pytest](https://pytest.org/)** — Testing

Coming in later phases: Twilio, SendGrid, HubSpot, Calendly, React.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

[MIT](./LICENSE)
