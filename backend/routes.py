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
        {"title": "Notes & Lecture Slides", "detail": "Operating Systems (Unit 3-4) and DBMS (Unit 2) notes uploaded by Prof. Lakshmi."},
        {"title": "Mid-2 Exam Schedule", "detail": "Timetable released. Exams start from October 20. Seating arrangements on ERP."},
        {"title": "Attendance Threshold", "detail": "CSE-III Section A average is 72%. Remember, 75% is required to avoid detention."},
        {"title": "Lab Schedule Shift", "detail": "DBMS Lab for batch B2 has been rescheduled to Thursday, 2:00 PM - 5:00 PM."},
        {"title": "Elective Registration", "detail": "Enrollment for ML and Cloud Computing electives is open until August 10."},
        {"title": "NPTEL Credit Transfer", "detail": "Submit your NPTEL course completion certificate to the HoD office before Nov 15."}
    ],
    "placements": [
        {"title": "TCS Placement Drive", "detail": "Drive on Aug 5. Eligible: CSE/IT/ECE (60%+ CGPA, no backlogs). Register by Aug 2."},
        {"title": "Amazon Hiring", "detail": "Drive on Sep 1. Eligible: CSE/IT (7.5%+ CGPA). Online test on HackerRank. Package: 12-18 LPA."},
        {"title": "Mock Interviews", "detail": "Conducted every Saturday from 10 AM. Book your slot on the placement portal."},
        {"title": "Resume Review Session", "detail": "Submit your draft resume by Wednesday to get personalized feedback on Friday."},
        {"title": "Zoho Summer Internships", "detail": "Applications open for pre-final year students. Deadline to apply is August 15."},
        {"title": "Placement Cell Contact", "detail": "Dr. Priya Sharma, placements@vidyuth.edu.in, Office: placement cell cabin."}
    ],
    "events": [
        {"title": "Yukti 2026 Tech Fest", "detail": "October 15-17. 50+ technical events including robot wars and drone racing."},
        {"title": "CodeSprint 5.0 Hackathon", "detail": "August 2-3. 36-hour coding challenge. Teams of 3-4. Prizes: Rs 50K/25K/10K."},
        {"title": "Gen AI & LLM Workshop", "detail": "August 10. Guest lecture by Dr. Ramesh Kumar (IIT Hyderabad). Limited to 120 seats."},
        {"title": "NSS Blood Donation Camp", "detail": "September 5, 9:00 AM - 2:00 PM in the college auditorium. Refreshments provided."},
        {"title": "LaunchPad Pitch Competition", "detail": "October 5. Pitch startup ideas to VCs. Prize pool of Rs 1,00,000."},
        {"title": "Photography Exhibition", "detail": "September 1-3. Submit your entries to the club president by August 25."}
    ],
    "hostel": [
        {"title": "Sri Sai Residency", "detail": "1.2 km away. Rs. 8,000/month. AC/Non-AC rooms. 3 vacancies left. Contact: +91-98765-43210."},
        {"title": "Green Valley PG", "detail": "0.8 km away. Rs. 6,500/month. 2/3 shared rooms. 5 beds available. Contact: +91-87654-32109."},
        {"title": "Campus Nest Hostel", "detail": "0.5 km away. Rs. 9,500/month. AC single/double. Fully booked, waitlist open. +91-76543-21098."},
        {"title": "Mess Timings", "detail": "Breakfast: 7:30-9:00 AM. Lunch: 12:30-2:00 PM. Dinner: 7:30-9:00 PM."},
        {"title": "Maintenance Desk", "detail": "Log requests at Warden Room 101. Standard response time is 48 hours."},
        {"title": "Warden Contact", "detail": "Mr. Venkatesh Reddy (+91-94321-56789), available 9:00 AM - 6:00 PM."}
    ],
    "support": [
        {"title": "Counseling & Wellness", "detail": "Book confidential sessions with Dr. Anitha Rao, Mon-Sat 9-5 in Room 205 Admin Block."},
        {"title": "Sahaya Peer Group", "detail": "Meets every Wednesday at 4:00 PM in the Student Activity Center. All are welcome."},
        {"title": "Campus Security Helpline", "detail": "Emergency contact: +91-40-2345-6792. Active 24/7. First aid available."},
        {"title": "Anti-Ragging Committee", "detail": "Contact Prof. K. Suresh, antiragging@vidyuth.edu.in. Toll-Free: 1800-180-5522."},
        {"title": "Yoga & Meditation", "detail": "Daily yoga sessions from 6:00 - 7:00 AM at the sports ground. Meditation room open 8 AM - 8 PM."}
    ],
}

DASHBOARD_CARDS = [
    {"title": "TCS Placement Drive", "detail": "Applications open for CSE/IT/ECE students. Register by August 2."},
    {"title": "Mid-2 Exam Schedule", "detail": "Exams start October 20. Seating arrangements and timetables published on ERP."},
    {"title": "CodeSprint 5.0 Hackathon", "detail": "Registrations open. Register your team of 3-4 by July 30. Cash prizes up to Rs 50,000."},
    {"title": "Attendance Warning", "detail": "12 students in CSE-III Section A below 75%. Submit condonation certificates by September 30."},
    {"title": "Gen AI & LLM Workshop", "detail": "August 10 by IIT Hyderabad faculty. Only 40 seats remaining. Register now."},
    {"title": "Hostel Vacancies", "detail": "Sri Sai Residency (3 rooms) and Green Valley PG (5 beds) have open slots."},
    {"title": "Counseling Slots Open", "detail": "Dr. Anitha Rao has counseling slots open. Book via student ERP portal."},
    {"title": "Library Notice", "detail": "New IEEE and Springer journal subscriptions activated. Log in using student credentials."},
    {"title": "Fee Payment Reminder", "detail": "Odd semester tuition fee due by August 31. Late fee of Rs 100/day applies after deadline."}
]

NOTIFICATIONS = [
    {"title": "Placement Cell", "detail": "TCS pre-placement talk on August 3 at 2:00 PM in Seminar Hall 1."},
    {"title": "Admin Office", "detail": "Online bonafide certificate requests submitted before 11:00 AM processed same-day."},
    {"title": "Exam Branch", "detail": "Mid-2 examination hall tickets will be available on the student ERP portal from October 15."},
    {"title": "Student Council", "detail": "Nominations open for Cultural Secretary. Submit your nomination forms by August 8."},
    {"title": "IT Department", "detail": "Campus WiFi maintenance scheduled for August 4, 2:00 AM - 6:00 AM. Expect downtime."},
    {"title": "Library Notice", "detail": "Overdue book returns deadline is August 1 to avoid a Rs. 5/day fine."}
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
