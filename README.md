# Campus Companion AI

## Problem Statement

College students often struggle to find clear, unified, and accurate information regarding college academics, hostel accommodations, placement schedules, administrative processes, and mental health support. Official portals are often fragmented, policies can be confusing, and manual queries to administration desks create long queues, administrative burden, and delays. 

## Project Description

**Campus Companion AI** is an AI-first student portal MVP. It offers a clean, routed dashboard for centralizing student needs. The core feature is an intent-aware student assistant powered by Google's Gemma 4. 

The application is structured to dynamically classify student queries, guide them empathetically through wellness protocols, draft structured grievances for infrastructure issues, and provide one-click navigation actions (e.g., routing directly to a placement portal or booking a counseling session). The assistant retrieves and grounds its answers on official campus markdown files, preventing hallucination and ensuring compliance with official institutional guidelines.

---

## Google AI Usage

### Tools / Models Used

- **Google Gemma 4** (specifically quantized `gemma4:e4b` running via local Ollama inference with customized context parameters for memory-constrained environments).

### Tech Stack used

- **Frontend:** React (Vite), Tailwind CSS, React Router DOM
- **Backend:** FastAPI (Python), Uvicorn, Pydantic, Requests
- **Orchestration:** Ollama API Client integration with custom CPU-fallback and timeout tuning.

### How Google AI Was Used

Google's Gemma 4 is integrated into the backend application to power the chat assistant:
1. **Query Processing:** When a user types a message, it is analyzed and classified into intents (`information`, `navigation`, `registration`, `grievance`, `support`).
2. **Retrieval-Augmented Generation (RAG):** The system dynamically matches the query against the official markdown policy files in the `/knowledge` folder.
3. **Prompt Injection:** The matched markdown context is injected into the system prompt along with policy guardrails.
4. **Structured Actions:** Gemma 4 uses this context to draft responses. It is instructed to never invent policies or deadlines and to output interactive buttons (navigation routes) to direct the user to the correct portal page.

---

### GitHub repo link of the project

[Campus Companion AI Repository](https://github.com/Meghanaadh/buildai)

## Proof of Google AI Usage

Include terminal inference logs or system prompt parameters in the [/proofs](file:///C:/Users/megha/.gemini/antigravity/scratch/buildai/proofs) folder.
<img width="1920" height="1020" alt="Screenshot 2026-07-18 063756" src="https://github.com/user-attachments/assets/50f91116-fcf6-40f9-ab9c-a55c2a568a7b" />

## Screenshots

Add project screenshots in [/screenshots](file:///C:/Users/megha/.gemini/antigravity/scratch/buildai/screenshots) folder.
<img width="1920" height="1020" alt="Screenshot 2026-07-18 063515" src="https://github.com/user-attachments/assets/3043b2d5-c3f9-4f2a-99fa-5b3ccb4ef441" />


---

## Demo Video

Uploaded demo video. [Watch Demo](https://drive.google.com/file/d/157ltCFCmgYZA3FWR2_uk9qslEHMXhNhJ/view?usp=drivesdk)
---

## Installation Steps

### Prerequisites
- Node.js & npm installed
- Python 3.10+ installed
- [Ollama](https://ollama.com) installed and running locally

### 1) Ollama Setup
Pull the Gemma 4 model:
```bash
ollama pull gemma4:e4b
```

### 2) Backend Setup
Navigate to the backend directory, create a virtual environment, install dependencies, and start the FastAPI server:
```bash
cd backend
python -m venv .venv
# On Windows (cmd):
.venv\Scripts\activate.bat
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3) Frontend Setup
Navigate to the frontend directory, install dependencies, and start the development server:
```bash
cd ../frontend
npm install
npm run dev
```

Open your browser and visit **http://localhost:5173** to view the app!
