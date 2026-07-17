from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

INTENT_RULES = [
    ("support", ["stressed", "anxious", "anxiety", "depressed", "counseling", "wellness"]),
    ("grievance", ["complaint", "issue", "not working", "broken", "problem", "ragging", "no water", "no internet", "damaged"]),
    ("navigation", ["open", "go to", "navigate", "take me", "show"]),
    ("registration", ["register", "registration", "apply", "enroll", "book", "slot"]),
]

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
    "placement": "placements",
    "event": "events",
    "hostel": "hostel",
    "support": "support",
    "counseling": "support",
}

ROUTE_BY_INTENT = {
    "registration": {"label": "Open Registration", "route": "/academics"},
    "grievance": {"label": "Open Hostel Complaint Form", "route": "/hostel"},
    "support": {"label": "Book Counseling", "route": "/support"},
}

SAFE_FALLBACK = (
    "I could not find an exact institutional policy in the current knowledge base. "
    "Please contact the concerned department office for official confirmation."
)


@dataclass
class ChatResult:
    reply: str
    intent: str
    actions: list[dict[str, str]]
    source: str


def _knowledge_root() -> Path:
    return Path(__file__).resolve().parent.parent / "knowledge"


def load_knowledge() -> dict[str, str]:
    root = _knowledge_root()
    knowledge: dict[str, str] = {}

    if not root.exists():
        return knowledge

    for file_path in root.glob("*.md"):
        knowledge[file_path.stem] = file_path.read_text(encoding="utf-8")

    return knowledge


def classify_intent(message: str) -> str:
    lowered = message.lower()
    for intent, words in INTENT_RULES:
        if any(word in lowered for word in words):
            return intent
    return "information"


def _route_from_message(message: str) -> dict[str, str] | None:
    lowered = message.lower()
    for module_name, action in MODULE_ACTIONS.items():
        if module_name in lowered:
            return action
    for alias, module_name in MODULE_ALIASES.items():
        if alias in lowered:
            return MODULE_ACTIONS[module_name]
    return None


def _module_from_message(message: str, available_modules: list[str]) -> str | None:
    lowered = message.lower()
    for module_name in available_modules:
        if module_name in lowered:
            return module_name
    if "transcript" in lowered or "bonafide" in lowered or "certificate" in lowered:
        return "administration"
    return None


def _extract_relevant_knowledge(message: str, knowledge: dict[str, str]) -> tuple[str, str]:
    module = _module_from_message(message, list(knowledge.keys()))
    if module and module in knowledge:
        return module, knowledge[module]

    combined = "\n\n".join(knowledge.values())
    return "knowledge_base", combined


def _build_grievance_reply(message: str) -> str:
    return (
        "I drafted a structured grievance for you:\n\n"
        "- Category: Hostel/Infrastructure Grievance\n"
        "- Student Description: "
        f"{message.strip()}\n"
        "- Severity: Medium (raise to High if safety risk is present)\n"
        "- Requested Action: Inspection and resolution timeline\n"
        "- Preferred Follow-up: Email and phone confirmation\n\n"
        "Please review and submit this through the hostel complaint form."
    )


def _build_support_reply(message: str) -> str:
    empathy = (
        "I am really sorry you are going through this. Your wellbeing matters, and support is available."
    )
    escalation = ""
    lowered = message.lower()
    if any(word in lowered for word in ["harm", "suicide", "panic attack", "unsafe", "emergency"]):
        escalation = (
            "\n\nIf you are in immediate danger, contact campus emergency services and trusted people nearby right away."
        )

    return (
        f"{empathy}\n\n"
        "You can take one small step now: pause, hydrate, and reach out to counseling support. "
        "I can route you to book a counseling appointment and share emergency contacts."
        f"{escalation}"
    )


def _prepare_prompt(intent: str, message: str, knowledge_snippet: str) -> str:
    return (
        "You are Campus Companion AI for a college.\n"
        "Rules:\n"
        "1) Never invent institutional policy or deadlines.\n"
        "2) Use only provided knowledge.\n"
        "3) If exact info is missing, say so and direct student to the appropriate department.\n"
        "4) Keep responses concise and actionable.\n\n"
        f"Intent: {intent}\n"
        f"Student Query: {message}\n\n"
        "Institutional Knowledge:\n"
        f"{knowledge_snippet[:12000]}"
    )


def _call_ollama(prompt: str) -> str | None:
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat"
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": "Respond safely and only with institutional knowledge."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {
            "num_gpu": 0,
            "num_ctx": 2048,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data.get("message", {}).get("content", "").strip() or None
    except (requests.RequestException, json.JSONDecodeError, ValueError):
        return None


def generate_chat_response(message: str) -> ChatResult:
    knowledge = load_knowledge()
    intent = classify_intent(message)
    actions: list[dict[str, str]] = []

    if intent == "navigation":
        action = _route_from_message(message) or MODULE_ACTIONS["dashboard"]
        actions.append(action)
        return ChatResult(
            reply=f"Sure, I can route you there now. Use the action below to continue to {action['label'].replace('Open ', '')}.",
            intent=intent,
            actions=actions,
            source="navigation",
        )

    if intent == "grievance":
        actions.append(ROUTE_BY_INTENT["grievance"])
        return ChatResult(
            reply=_build_grievance_reply(message),
            intent=intent,
            actions=actions,
            source="grievance_template",
        )

    if intent == "support":
        actions.append(ROUTE_BY_INTENT["support"])
        return ChatResult(
            reply=_build_support_reply(message),
            intent=intent,
            actions=actions,
            source="support_protocol",
        )

    knowledge_source, knowledge_text = _extract_relevant_knowledge(message, knowledge)
    prompt = _prepare_prompt(intent, message, knowledge_text)
    model_reply = _call_ollama(prompt)

    if intent == "registration":
        actions.append(ROUTE_BY_INTENT["registration"])

    module_action = _route_from_message(message)
    if module_action and module_action not in actions:
        actions.append(module_action)

    if model_reply:
        return ChatResult(reply=model_reply, intent=intent, actions=actions, source=knowledge_source)

    fallback_reply = (
        "I could not reach the Gemma model right now, so I am using safe fallback guidance.\n\n"
        f"{SAFE_FALLBACK}"
    )
    if knowledge_source == "administration":
        fallback_reply += "\nFor transcript/bonafide help, please contact the Administration Office."
    return ChatResult(reply=fallback_reply, intent=intent, actions=actions, source="fallback")
