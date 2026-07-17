from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import requests

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

INTENT_KEYWORDS: dict[str, set[str]] = {
    "navigation": {"open", "show", "go to", "navigate", "take me", "book"},
    "registration": {"register", "apply", "enroll", "sign up", "join"},
    "grievance": {"complaint", "issue", "not working", "problem", "damaged", "no water", "ragging"},
    "support": {"stressed", "stress", "anxious", "anxiety", "counsel", "mental", "depressed", "panic"},
    "information": {"how", "when", "where", "what", "who", "policy", "procedure", "schedule"},
}

INTENT_TO_ROUTE = {
    "navigation": "/dashboard",
    "registration": "/placements",
    "grievance": "/support",
    "support": "/support",
    "information": "/academics",
}

SECTION_TO_ROUTE = {
    "academics": "/academics",
    "placements": "/placements",
    "events": "/events",
    "hostel": "/hostel",
    "administration": "/dashboard",
    "support": "/support",
}


def classify_intent(message: str) -> str:
    text = message.lower().strip()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "information"


def _normalize_tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z]{3,}", text.lower())}


def _load_knowledge() -> dict[str, str]:
    docs: dict[str, str] = {}
    for file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        docs[file.stem] = file.read_text(encoding="utf-8")
    return docs


def _best_knowledge_match(query: str, docs: dict[str, str]) -> tuple[str | None, str | None]:
    query_tokens = _normalize_tokens(query)
    if not query_tokens:
        return None, None

    best_doc = None
    best_score = 0

    for section, content in docs.items():
        score = len(query_tokens.intersection(_normalize_tokens(content)))
        if score > best_score:
            best_score = score
            best_doc = section

    if best_doc is None or best_score == 0:
        return None, None

    content = docs[best_doc]
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    snippet = "\n".join(lines[:5])
    return best_doc, snippet


def _department_fallback(section: str | None) -> str:
    department = (section or "the relevant").replace("_", " ").title()
    return (
        f"I couldn't find a verified policy for that in the knowledge base. "
        f"Please contact the {department} department for confirmation."
    )


def _complaint_draft(message: str) -> str:
    return (
        "Here is a structured complaint draft:\n"
        "Subject: Infrastructure Issue Report\n"
        "Description: "
        f"{message.strip()}\n"
        "Requested Action: Kindly inspect and resolve this issue at the earliest.\n"
        "Student Details: [Name, Department, Year, Contact]"
    )


def _support_reply(message: str, support_snippet: str | None) -> str:
    base = (
        "I'm sorry you're feeling this way. You're not alone, and it's okay to ask for help. "
        "Try a short break, hydrate, and do a 2-minute breathing reset. "
        "If this continues, please book a counseling appointment through Student Support."
    )
    if support_snippet:
        return f"{base}\n\nCampus support options:\n{support_snippet}"
    return base


def _call_ollama(prompt: str) -> str | None:
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "gemma:4b", "prompt": prompt, "stream": False},
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
        text = payload.get("response")
        if isinstance(text, str) and text.strip():
            return text.strip()
    except (requests.RequestException, ValueError):
        return None
    return None


def respond_to_student(message: str) -> dict[str, Any]:
    intent = classify_intent(message)
    docs = _load_knowledge()
    matched_section, snippet = _best_knowledge_match(message, docs)

    if intent == "grievance":
        content = _complaint_draft(message)
    elif intent == "support":
        support_snippet = docs.get("support", "")
        content = _support_reply(message, support_snippet[:400] if support_snippet else None)
    elif snippet:
        guard_prompt = (
            "Answer only using the provided campus knowledge. "
            "If information is missing, explicitly say to contact the department.\n\n"
            f"Question: {message}\n\n"
            f"Knowledge:\n{snippet}\n"
        )
        content = _call_ollama(guard_prompt) or f"Based on campus information:\n{snippet}"
    else:
        content = _department_fallback(matched_section)

    if not snippet and intent in {"information", "registration", "navigation"}:
        content = _department_fallback(matched_section)

    route = SECTION_TO_ROUTE.get(matched_section or "", INTENT_TO_ROUTE[intent])
    action_labels = {
        "navigation": "Open Service",
        "registration": "Open Registration",
        "grievance": "Open Complaint Form",
        "support": "Book Counseling",
        "information": "Open Relevant Module",
    }

    return {
        "intent": intent,
        "answer": content,
        "action": {
            "label": action_labels[intent],
            "route": route,
        },
        "source": matched_section,
    }
