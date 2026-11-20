# MediTrack 💊

> **Medication adherence tracking for people living with chronic conditions**

[![CI](https://github.com/kareemrt/clauder/actions/workflows/ci.yml/badge.svg)](https://github.com/kareemrt/clauder/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-16%20passed-brightgreen)](tests/)

---

## The Problem

```
  50% of patients with chronic conditions don't take their medications as prescribed.

  This causes:
    ✗  125,000 preventable deaths per year in the United States
    ✗  $100–300 billion in avoidable healthcare costs annually
    ✗  Disease progression, hospitalizations, and reduced quality of life
```

Existing reminder apps are either too complex, require cloud accounts, or don't give
doctors the adherence data they actually need. MediTrack is the tool that fills that gap —
simple, private, and built around the patient-doctor workflow.

---

## What MediTrack Does

MediTrack is a **local-first web application** that helps patients:

- **Manage** all their medications in one place (name, dosage, frequency, instructions)
- **Log doses** daily and mark them taken with one click
- **Track symptoms** with severity ratings and free-text notes
- **Review adherence statistics** over any time window (day, week, month, year)
- **Share health reports** with their doctor at appointments

Everything runs on your machine. No accounts. No data uploaded anywhere.

---

## Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  💊 MediTrack          Dashboard  Medications  API Docs      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │    3     │  │  87.5%   │  │    4     │  │    2     │   │
│  │ Active   │  │ 30-Day   │  │  Doses   │  │ Remaining│   │
│  │   Meds   │  │Adherence │  │  Today   │  │  Today   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  Today's Doses               │  Log a Symptom               │
│  ─────────────               │  ─────────────               │
│  ■ Metformin 500mg   ✓ Taken │  Symptom: [Headache      ]  │
│  ■ Lisinopril 10mg   Pending │  Severity: ──────●─── 7/10  │
│  ■ Atorvastatin 20mg ✓ Taken │  Notes:  [optional...   ]   │
│                   [+ Log]    │          [   Log Symptom  ]  │
│                                                              │
│  Medication Adherence (Last 30 Days)                         │
│  ────────────────────────────────────                        │
│  Metformin     ████████████████████░░░   90%                │
│  Lisinopril    █████████████░░░░░░░░░░   62%                │
│  Atorvastatin  ████████████████████████  100%               │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| 📋 **Medication Management** | Add, edit, and deactivate medications with full details |
| ✅ **One-Click Dose Logging** | Mark today's doses taken directly from the dashboard |
| 📊 **Adherence Visualization** | Color-coded adherence bars (green ≥80%, yellow 50–79%, red <50%) |
| 🩺 **Symptom Journal** | Log symptoms 1–10 severity with timestamps and notes |
| 📈 **Health Summary API** | Structured JSON reports for integration with other health tools |
| 🔒 **Privacy-First** | SQLite database stored locally — zero cloud dependencies |
| 🐳 **Docker Support** | One command to run anywhere |
| 🧪 **Full Test Suite** | 16 integration tests covering all API endpoints |
| 📖 **Auto-generated API Docs** | Interactive Swagger UI at `/docs` |

---

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                        Browser                            │
│   index.html  dashboard.html  medications.html            │
│        │             │                │                   │
│   app.js        dashboard.js    medications.js            │
└──────────────────────┬────────────────────────────────────┘
                       │  HTTP (REST JSON)
┌──────────────────────▼────────────────────────────────────┐
│                   FastAPI Server                           │
│                                                           │
│   /api/medications/   /api/doses/    /api/symptoms/       │
│         │                 │               │               │
│         └─────────────────┴───────────────┘               │
│                           │                               │
│               SQLAlchemy ORM                              │
└──────────────────────────┬────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────┐
│               SQLite Database (meditrack.db)               │
│                                                           │
│   medications   │   dose_logs   │   symptom_logs          │
└───────────────────────────────────────────────────────────┘
```

### Data Model

```
medications
  id, name, dosage, frequency, times_per_day,
  instructions, start_date, end_date, is_active

dose_logs
  id, medication_id → medications,
  scheduled_time, taken_at, was_taken, notes

symptom_logs
  id, symptom, severity (1–10), notes, logged_at
```

---

## Quick Start

### Option 1: Run directly (Python 3.11+)

```bash
# Clone the repository
git clone https://github.com/kareemrt/clauder.git
cd clauder

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000

# Open in your browser
open http://localhost:8000
```

### Option 2: Docker

```bash
docker compose up
# → http://localhost:8000
```

### Option 3: Docker (single container)

```bash
docker build -t meditrack .
docker run -p 8000:8000 -v $(pwd)/data:/app/data meditrack
```

---

## API Reference

The full interactive API documentation is available at **`/docs`** (Swagger UI) or **`/redoc`** (ReDoc).

### Endpoints

```
Medications
  GET    /api/medications/           List all medications
  POST   /api/medications/           Create a medication
  GET    /api/medications/{id}       Get one medication
  PATCH  /api/medications/{id}       Update a medication
  DELETE /api/medications/{id}       Delete a medication

Doses
  GET    /api/doses/                 List dose logs (filter by medication, days)
  GET    /api/doses/today            Today's dose schedule
  POST   /api/doses/                 Log a dose
  PATCH  /api/doses/{id}             Update a dose log
  POST   /api/doses/{id}/take        Mark a dose as taken (sets taken_at = now)

Symptoms
  GET    /api/symptoms/              List symptom logs (filter by days)
  POST   /api/symptoms/              Log a symptom
  DELETE /api/symptoms/{id}          Delete a symptom log

Reports
  GET    /api/reports/adherence      Per-medication adherence rates
  GET    /api/reports/summary        Full health summary (dashboard data)

Utility
  GET    /health                     Health check
  GET    /docs                       Swagger UI
```

### Example: Create a medication

```bash
curl -X POST http://localhost:8000/api/medications/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Metformin",
    "dosage": "500mg",
    "frequency": "twice daily with meals",
    "times_per_day": 2,
    "instructions": "Take with food to reduce GI side effects"
  }'
```

```json
{
  "id": 1,
  "name": "Metformin",
  "dosage": "500mg",
  "frequency": "twice daily with meals",
  "times_per_day": 2,
  "instructions": "Take with food to reduce GI side effects",
  "start_date": "2026-11-20T11:14:00",
  "end_date": null,
  "is_active": true,
  "created_at": "2026-11-20T11:14:00"
}
```

### Example: Get 30-day adherence report

```bash
curl http://localhost:8000/api/reports/adherence?days=30
```

```json
[
  {
    "medication_id": 1,
    "medication_name": "Metformin",
    "total_scheduled": 60,
    "total_taken": 54,
    "adherence_rate": 90.0,
    "period_days": 30
  }
]
```

---

## Project Structure

```
meditrack/
├── app/
│   ├── main.py          # FastAPI app entry point, routes
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # ORM models (Medication, DoseLog, SymptomLog)
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── medications.py
│       ├── doses.py
│       ├── symptoms.py
│       └── reports.py
├── static/
│   ├── css/style.css    # All styling
│   └── js/
│       ├── app.js       # Shared utilities (API client, toast, formatters)
│       ├── dashboard.js # Dashboard page logic
│       └── medications.js
├── templates/
│   ├── index.html       # Landing page
│   ├── dashboard.html   # Main dashboard
│   └── medications.html # Medication management
├── tests/
│   └── test_api.py      # 16 integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
    └── workflows/ci.yml # CI: tests + ruff linting
```

---

## Development

```bash
# Run tests
pytest tests/ -v

# Run with hot reload
uvicorn app.main:app --reload

# Lint
pip install ruff
ruff check app/
```

### Running tests

```
$ pytest tests/ -v

tests/test_api.py::test_create_medication          PASSED
tests/test_api.py::test_list_medications_empty     PASSED
tests/test_api.py::test_list_medications           PASSED
tests/test_api.py::test_get_medication             PASSED
tests/test_api.py::test_get_medication_not_found   PASSED
tests/test_api.py::test_update_medication          PASSED
tests/test_api.py::test_delete_medication          PASSED
tests/test_api.py::test_log_dose                   PASSED
tests/test_api.py::test_mark_dose_taken            PASSED
tests/test_api.py::test_log_dose_invalid_medication PASSED
tests/test_api.py::test_log_symptom                PASSED
tests/test_api.py::test_symptom_severity_validation PASSED
tests/test_api.py::test_list_symptoms              PASSED
tests/test_api.py::test_health_summary_empty       PASSED
tests/test_api.py::test_adherence_report           PASSED
tests/test_api.py::test_health_endpoint            PASSED

16 passed in 1.45s
```

---

## Roadmap

- [ ] Browser push notifications for dose reminders
- [ ] Export health reports as PDF
- [ ] Multi-user support with authentication
- [ ] Medication interaction checker (via open drug APIs)
- [ ] Mobile-optimized PWA (installable on phone)
- [ ] Caregiver view — family members can track adherence for loved ones
- [ ] Integration with Apple Health / Google Fit

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Write tests for your changes
4. Run the test suite (`pytest tests/ -v`)
5. Open a pull request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Why This Matters

> *"The drugs don't work in patients who don't take them."*
> — C. Everett Koop, former U.S. Surgeon General

Medication non-adherence is one of the most solvable problems in modern healthcare.
MediTrack is a step toward giving patients the tools to stay on track — without
sacrificing their privacy or overwhelming them with complexity.

---

*Built with [FastAPI](https://fastapi.tiangolo.com) · [SQLAlchemy](https://sqlalchemy.org) · [SQLite](https://sqlite.org)*
