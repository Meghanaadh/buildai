from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from gemma import respond_to_student

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class Action(BaseModel):
    label: str
    route: str


class ChatResponse(BaseModel):
    reply: str
    intent: Literal["information", "navigation", "registration", "grievance", "support"]
    actions: list[Action] = Field(default_factory=list)
    source: str


class Item(BaseModel):
    title: str
    detail: str


class ListResponse(BaseModel):
    items: list[Item]


DASHBOARD_CARDS = [
    {"title": "Placement Notifications", "detail": "6 new"},
    {"title": "Course Registration", "detail": "Open"},
    {"title": "Upcoming Events", "detail": "4 this week"},
    {"title": "Academic Notes", "detail": "12 updated"},
    {"title": "Hostel Availability", "detail": "8 rooms"},
    {"title": "Mental Wellness", "detail": "Counseling available"},
    {"title": "Recent Announcements", "detail": "5 unread"},
]

NOTIFICATION_ITEMS = [
    {"title": "Registration Window", "detail": "Course registration closes on Friday, 5 PM."},
    {"title": "Placements", "detail": "Mock interview slots are open for final-year students."},
    {"title": "Wellness", "detail": "Mental wellness workshop starts tomorrow at 11 AM."},
]

MODULE_DATA = {
    "academics": [
        {"title": "Notes", "detail": "Department notes are updated weekly."},
        {"title": "Exam Schedule", "detail": "Mid-semester exams start from 12 Aug."},
        {"title": "Course Registration", "detail": "Course registration portal is open for this semester."},
    ],
    "placements": [
        {"title": "Upcoming Companies", "detail": "Apex Labs and CoreNova hiring this month."},
        {"title": "Mock Interview", "detail": "Registration open until Friday."},
        {"title": "Resume Tips", "detail": "Placement cell review slots available every Tuesday."},
    ],
    "events": [
        {"title": "Hackathon", "detail": "Campus CodeSprint starts 25 July."},
        {"title": "Workshops", "detail": "AI workshop registrations close tomorrow."},
    ],
    "hostel": [
        {"title": "Hostel Complaints", "detail": "Raise complaints via support desk with room details."},
        {"title": "Vacant Rooms", "detail": "8 rooms currently available in Block C."},
    ],
    "support": [
        {"title": "Counseling", "detail": "Book sessions through student support portal."},
        {"title": "Emergency Contact", "detail": "Use support line +91-00000-00000 for urgent help."},
    ],
}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = respond_to_student(request.message)
    return ChatResponse(
        reply=result.get("reply", ""),
        intent=result.get("intent", "information"),
        actions=result.get("actions", []),
        source=result.get("source") or "unknown",
    )


@router.get("/dashboard/cards", response_model=ListResponse)
def dashboard_cards() -> ListResponse:
    return ListResponse(items=DASHBOARD_CARDS)


@router.get("/notifications", response_model=ListResponse)
def notifications() -> ListResponse:
    return ListResponse(items=NOTIFICATION_ITEMS)


@router.get("/modules/{module_name}", response_model=ListResponse)
def module_data(module_name: str) -> ListResponse:
    items = MODULE_DATA.get(module_name.lower())
    if items is None:
        raise HTTPException(status_code=404, detail=f"Unknown module: {module_name}")
    return ListResponse(items=items)


@router.get("/dashboard", response_model=ListResponse)
def dashboard_legacy() -> ListResponse:
    return dashboard_cards()


@router.get("/module/{module_name}", response_model=ListResponse)
def module_legacy(module_name: str) -> ListResponse:
    return module_data(module_name)
