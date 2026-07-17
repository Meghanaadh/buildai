# Campus Companion AI

Campus Companion AI is a centralized student portal where **Gemma 4** is the primary interface for academics, placements, events, hostel services, administration support, grievances, and mental wellness guidance.

## Project Structure

- `/frontend` — React (Vite) + Tailwind + React Router student portal UI
- `/backend` — FastAPI service for chat orchestration, intent classification, routing, and module APIs
- `/knowledge` — markdown-based institutional knowledge base used by Gemma

## Core Architecture

1. Student asks a question in Assistant.
2. Backend classifies intent (`information`, `navigation`, `registration`, `grievance`, `support`).
3. Relevant markdown knowledge is retrieved.
4. Gemma response is generated using Ollama when available, with strict grounding behavior.
5. UI receives response + action button route and navigates to a module.

## Safety Rules

- Policies are grounded to the knowledge base only.
- If relevant information is unavailable, the assistant asks students to contact the appropriate department.
- Grievance messages produce a structured complaint draft.

## Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- (Optional for live LLM) Ollama with Gemma model running locally

### Frontend

```bash
cd /home/runner/work/buildai/buildai/frontend
npm install
npm run dev
```

Default app URL: `http://127.0.0.1:5173`

### Backend

```bash
cd /home/runner/work/buildai/buildai/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Default API URL: `http://127.0.0.1:8000`

To point frontend to a different backend:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api npm run dev
```

## API Contracts

- `POST /api/chat` with `{ "message": "..." }`
  - returns: `intent`, `answer`, `action { label, route }`, `source`
- `GET /api/dashboard`
  - returns dashboard cards
- `GET /api/notifications`
  - returns recent notification items
- `GET /api/module/{module_name}`
  - returns module-specific list items

## Knowledge Base Files

- `/knowledge/academics.md`
- `/knowledge/placements.md`
- `/knowledge/events.md`
- `/knowledge/hostel.md`
- `/knowledge/administration.md`
- `/knowledge/support.md`

Each file uses section-based headings so retrieval can remain predictable.

## Future Extensibility

This implementation is designed to support:

- RAG over PDFs and databases
- multilingual response support
- voice assistant integration
- authentication/student login
- notifications and calendar/email integration
- ERP integrations and analytics dashboards
