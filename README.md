# Campus Companion AI

[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com/deploy?repo=https://github.com/Meghanaadh/buildai)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FMeghanaadh%2Fbuildai&root-directory=frontend)

Campus Companion AI is an AI-first student portal MVP where Gemma (via Ollama) is the primary interface for academics, placements, events, hostel, administration, grievance, and wellness support.

## Architecture

- **Frontend**: React (Vite), Tailwind CSS, React Router (`frontend/`)
- **Backend**: FastAPI (`backend/`)
- **AI orchestration**: Gemma integration via Ollama (`backend/gemma.py`)
- **Knowledge base**: Markdown files in `knowledge/`

## Repository Structure

- `frontend/` React app with routed pages, shared components, and API client
- `backend/` FastAPI app, routes, and Gemma orchestration logic
- `knowledge/` institutional markdown knowledge files

## Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2) Ollama + Gemma

Install Ollama, then pull and run a Gemma model (example):

```bash
ollama pull gemma3:4b
```

Optional environment variables for backend:

- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_MODEL` (default: `gemma3:4b`)

### 3) Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional frontend environment variable:

- `VITE_API_BASE_URL` (default: `http://localhost:8000`)

## API Contracts

### `POST /chat`

Request body:

```json
{
  "message": "How do I apply for a transcript?",
  "history": [
    { "role": "user", "content": "Hi" },
    { "role": "assistant", "content": "Hello" }
  ]
}
```

Response body:

```json
{
  "reply": "...",
  "intent": "information",
  "actions": [{ "label": "Open Registration", "route": "/academics" }],
  "source": "administration"
}
```

### Other endpoints

- `GET /health`
- `GET /dashboard/cards`
- `GET /notifications`
- `GET /modules/{module_name}`

## Product Behavior

- Intent categories: `information`, `navigation`, `registration`, `grievance`, `support`
- Knowledge-grounded responses from markdown files under `knowledge/`
- Guardrail fallback used when policy details are missing or model is unavailable
- Grievance flow creates structured complaint draft and complaint-routing action
- Support flow returns empathetic guidance and emergency escalation language for high-risk terms
- Navigation flow returns action metadata for direct module routing

## Known Limitations

- Current retrieval is file-level heuristic matching, not full semantic RAG.
- Live institutional data integration (ERP/auth/calendar) is not connected.
- Model quality depends on local Ollama and available Gemma model.

## Future Extensions

- PDF + database RAG with chunking and embeddings
- Multilingual assistant responses
- Voice interface
- ERP hooks for authenticated student actions
- Calendar and alert integrations
- Personalized notification and analytics layer
