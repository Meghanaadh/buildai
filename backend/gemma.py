from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import requests

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:4b")

INTENT_KEYWORDS: dict[str, set[str]] = {
    "navigation": {"open", "show", "go to", "navigate", "take me"},
    "registration": {"register", "enroll", "sign up", "join"},
    "grievance": {"complaint", "issue", "not working", "problem", "damaged", "no water", "ragging"},
    "support": {"stressed", "stress", "anxious", "anxiety", "counsel", "mental", "depressed", "panic"},
    "information": {
        "how",
        "when",
        "where",
        "what",
        "who",
        "policy",
        "procedure",
        "schedule",
        "transcript",
        "bonafide",
    },
}

INTENT_TO_ROUTE = {
    "navigation": "/dashboard",
    "registration": "/academics",
    "grievance": "/hostel",
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

SECTION_HINTS: dict[str, set[str]] = {
    "administration": {"transcript", "bonafide", "certificate", "administration", "document"},
    "academics": {"exam", "attendance", "notes", "course", "semester", "subject"},
    "placements": {"placement", "company", "resume", "interview", "recruiter", "job"},
    "events": {"event", "hackathon", "workshop", "club", "fest"},
    "hostel": {"hostel", "room", "mess", "water", "maintenance"},
    "support": {"support", "counseling", "anxiety", "stress", "wellness", "mental"},
}

MODULE_ACTIONS = {
    "academics": {"label": "Open Academics", "route": "/academics"},
    "placements": {"label": "Open Placements", "route": "/placements"},
    "events": {"label": "Open Events", "route": "/events"},
    "hostel": {"label": "Open Hostel", "route": "/hostel"},
    "support": {"label": "Book Counseling", "route": "/support"},
    "dashboard": {"label": "Open Dashboard", "route": "/dashboard"},
}

MODULE_ALIASES = {
    "academic": "academics",
    "academics": "academics",
    "placement": "placements",
    "placements": "placements",
    "event": "events",
    "events": "events",
    "hostel": "hostel",
    "support": "support",
    "counseling": "support",
    "dashboard": "dashboard",
}


def classify_intent(message: str) -> str:
    text = message.lower().strip()
    scores = {
        intent: sum(1 for keyword in keywords if keyword in text)
        for intent, keywords in INTENT_KEYWORDS.items()
    }
    if "book" in text and ("counsel" in text or "appointment" in text):
        scores["support"] += 1
    if "apply" in text and ("transcript" in text or "bonafide" in text):
        scores["information"] += 2

    best_intent = max(scores, key=scores.get)
    if scores[best_intent] > 0:
        return best_intent
    return "information"


def _normalize_tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z]{3,}", text.lower())}


def _load_knowledge() -> dict[str, str]:
    docs: dict[str, str] = {}
    if not KNOWLEDGE_DIR.exists():
        return docs

    for file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        docs[file.stem] = file.read_text(encoding="utf-8")
    return docs


def _best_knowledge_match(query: str, docs: dict[str, str]) -> tuple[str | None, str | None]:
    normalized_query = query.lower()

    for section, hints in SECTION_HINTS.items():
        if section in docs and any(hint in normalized_query for hint in hints):
            content = docs[section]
            lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
            return section, "\n".join(lines[:5])

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
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
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


def _route_from_message(message: str) -> dict[str, str] | None:
    lowered = message.lower()
    for alias, module_name in MODULE_ALIASES.items():
        if alias in lowered:
            return MODULE_ACTIONS[module_name]
    return None


def respond_to_student(message: str) -> dict[str, Any]:
    intent = classify_intent(message)
    docs = _load_knowledge()
    matched_section, snippet = _best_knowledge_match(message, docs)

    if intent == "grievance":
        return {
            "reply": _complaint_draft(message),
            "intent": intent,
            "actions": [MODULE_ACTIONS["hostel"]],
            "source": "grievance_template",
        }
    if intent == "support":
        support_snippet = docs.get("support", "")
        return {
            "reply": _support_reply(message, support_snippet[:400] if support_snippet else None),
            "intent": intent,
            "actions": [MODULE_ACTIONS["support"]],
            "source": "support_protocol",
        }
    if intent == "navigation":
        action = _route_from_message(message) or MODULE_ACTIONS["dashboard"]
        return {
            "reply": (
                f"Sure, I can route you there now. Use the action below to continue to "
                f"{action['label'].replace('Open ', '')}."
            ),
            "intent": intent,
            "actions": [action],
            "source": "navigation",
        }

    if snippet:
        guard_prompt = (
            "Answer only using the provided campus knowledge. "
            "If information is missing, explicitly say to contact the department.\n\n"
            f"Question: {message}\n\n"
            f"Knowledge:\n{snippet}\n"
        )
        content = _call_ollama(guard_prompt) or f"Based on campus information:\n{snippet}"
        source = matched_section or "knowledge_base"
    else:
        content = _department_fallback(matched_section)
        source = "knowledge_fallback"

    route = SECTION_TO_ROUTE.get(matched_section or "", INTENT_TO_ROUTE[intent])
    action_label = "Open Registration" if intent == "registration" else "Open Relevant Module"
    actions = [{"label": action_label, "route": route}] if route else []

    return {
        "reply": content,
        "intent": intent,
        "actions": actions,
        "source": source,
    }
