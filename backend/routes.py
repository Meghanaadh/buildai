from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from gemma import respond_to_student

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest) -> dict:
    return respond_to_student(request.message)


@router.get("/notifications")
def notifications() -> dict:
    return {
        "items": [
            "Course registration closes on Friday, 5 PM.",
            "Mock interview slots are open for final-year students.",
            "Mental wellness workshop starts tomorrow at 11 AM.",
        ]
    }


@router.get("/dashboard")
def dashboard_data() -> dict:
    return {
        "cards": [
            {"title": "Placement Notifications", "value": "6 new"},
            {"title": "Course Registration", "value": "Open"},
            {"title": "Upcoming Events", "value": "4 this week"},
            {"title": "Academic Notes", "value": "12 updated"},
            {"title": "Hostel Availability", "value": "8 rooms"},
            {"title": "Mental Wellness", "value": "Counseling available"},
            {"title": "Recent Announcements", "value": "5 unread"},
        ]
    }


@router.get("/module/{module_name}")
def module_data(module_name: str) -> dict:
    module_map = {
        "academics": ["Notes", "Exam Schedule", "Course Registration", "Attendance Information"],
        "placements": ["Placement Notifications", "Upcoming Companies", "Resume Tips", "Mock Interview Registration"],
        "events": ["Hackathons", "Workshops", "Club Activities"],
        "hostel": ["Nearby Hostels", "Vacant Rooms", "Hostel Rules", "Hostel Complaints"],
        "support": ["Mental Wellness", "Counseling Appointment", "Anti-Ragging", "Emergency Contacts"],
    }
    return {"module": module_name, "items": module_map.get(module_name, [])}
