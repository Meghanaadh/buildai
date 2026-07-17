from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from gemma import generate_chat_response

router = APIRouter()


class Action(BaseModel):
    label: str
    route: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[Message] = Field(default_factory=list)


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


MODULE_DATA = {
    "academics": [
        {"title": "Notes", "detail": "Department notes are updated weekly."},
        {"title": "Exam Schedule", "detail": "Mid-semester exams start from 12 Aug."},
    ],
    "placements": [
        {"title": "Upcoming Companies", "detail": "Apex Labs and CoreNova hiring this month."},
        {"title": "Mock Interview", "detail": "Registration open until Friday."},
    ],
    "events": [
        {"title": "Hackathon", "detail": "Campus CodeSprint starts 25 July."},
        {"title": "Workshop", "detail": "AI for Robotics workshop on Saturday."},
    ],
    "hostel": [
        {"title": "Vacancies", "detail": "8 shared rooms available near north gate."},
        {"title": "Complaint Desk", "detail": "Submit maintenance grievances online."},
    ],
    "support": [
        {"title": "Counseling", "detail": "Book sessions Mon-Sat between 9 AM and 5 PM."},
        {"title": "Emergency", "detail": "Campus helpline: +91-00000-00000."},
    ],
}

DASHBOARD_CARDS = [
    {"title": "Placement Notifications", "detail": "2 companies opened applications this week."},
    {"title": "Course Registration", "detail": "Elective registration opens Monday."},
    {"title": "Upcoming Events", "detail": "Hackathon, workshops, and clubs this week."},
    {"title": "Academic Notes", "detail": "Operating Systems notes updated in portal."},
    {"title": "Hostel Availability", "detail": "8 rooms available in nearby hostels."},
    {"title": "Mental Wellness", "detail": "Counseling appointment slots are open."},
    {"title": "Recent Announcements", "detail": "Bonafide process now supports online request."},
]

NOTIFICATIONS = [
    {"title": "Admin Office", "detail": "Transcript requests take 3-5 working days."},
    {"title": "Placement Cell", "detail": "Resume screening session this Friday."},
    {"title": "Support Center", "detail": "Wellness group session at 4 PM today."},
]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = generate_chat_response(request.message)
    return ChatResponse(reply=result.reply, intent=result.intent, actions=result.actions, source=result.source)


@router.get("/dashboard/cards", response_model=ListResponse)
def dashboard_cards() -> ListResponse:
    return ListResponse(items=DASHBOARD_CARDS)


@router.get("/notifications", response_model=ListResponse)
def notifications() -> ListResponse:
    return ListResponse(items=NOTIFICATIONS)


@router.get("/modules/{module_name}", response_model=ListResponse)
def module_data(module_name: str) -> ListResponse:
    key = module_name.lower()
    if key not in MODULE_DATA:
        raise HTTPException(status_code=404, detail="Module not found")
    return ListResponse(items=MODULE_DATA[key])
