"""
Generate Data_Calendar.json với dữ liệu phong phú từ hôm nay (07/05/2026)
đến 60 ngày sau. Mỗi ngày có 2-5 activities ngẫu nhiên.

Usage: python generate_calendar.py
Output: Data_Calendar.json
"""
import json
import random
from datetime import datetime, timedelta

# Hôm nay
TODAY = datetime(2026, 5, 7)
NUM_DAYS = 60

# Templates đa dạng cho activities
MEETING_TITLES = [
    "Team Standup", "Sprint Planning", "Sprint Review", "Sprint Retrospective",
    "Product Roadmap Discussion", "Stakeholder Meeting", "Customer Demo",
    "Code Review Session", "Architecture Review", "Tech Talk",
    "1-on-1 with Manager", "Quarterly Business Review", "Budget Planning",
    "Marketing Strategy Meeting", "Sales Pipeline Review", "HR Sync",
    "Engineering All-Hands", "Design Critique", "API Design Review",
    "Performance Review", "Hiring Panel Interview", "Vendor Meeting",
    "Client Onboarding Call", "Project Status Update", "Risk Assessment",
]

EVENT_TITLES = [
    "Morning Yoga", "Gym Workout", "Team Lunch", "Coffee with Mentor",
    "Read Programming Book", "Online Course - ML Basics", "Side Project Coding",
    "Personal Reflection", "Family Dinner", "Movie Night", "Chess Practice",
    "Language Learning - Japanese", "Cooking Class", "Photography Walk",
    "Volunteer at Shelter", "Doctor Appointment", "Dentist Check-up",
    "Hair Salon", "Grocery Shopping", "House Cleaning", "Laundry Day",
    "Date Night", "Book Club Meeting", "Birthday Party", "Wedding Anniversary",
    "Concert Tickets", "Art Exhibition", "Football Match", "Hiking Trip",
    "Beach Day", "Meditation Session", "Therapy Appointment",
]

# Time slots tự nhiên cho meeting (giờ làm việc)
MEETING_SLOTS = [
    ("09:00", "10:00"), ("09:30", "10:30"), ("10:00", "11:00"),
    ("10:30", "11:30"), ("11:00", "12:00"), ("13:00", "14:00"),
    ("13:30", "14:30"), ("14:00", "15:00"), ("14:30", "15:30"),
    ("15:00", "16:00"), ("15:30", "16:30"), ("16:00", "17:00"),
]

# Time slots cho event (cả ngày)
EVENT_START_TIMES = [
    "06:00", "06:30", "07:00", "07:30", "08:00", "12:00", "12:30",
    "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "21:00",
]


def random_meeting():
    start, end = random.choice(MEETING_SLOTS)
    return {
        "type": "meeting",
        "description": random.choice(MEETING_TITLES),
        "start_time": start,
        "end_time": end,
    }


def random_event():
    start = random.choice(EVENT_START_TIMES)
    # 50% có end_time, 50% null
    if random.random() < 0.5:
        h, m = map(int, start.split(":"))
        duration_h = random.choice([1, 1, 2])  # đa số 1h, đôi khi 2h
        end_h = min(h + duration_h, 23)
        end = f"{end_h:02d}:{m:02d}"
        return {
            "type": "event",
            "description": random.choice(EVENT_TITLES),
            "start_time": start,
            "end_time": end,
        }
    return {
        "type": "event",
        "description": random.choice(EVENT_TITLES),
        "start_time": start,
        "end_time": None,
    }


def generate_day(date_obj):
    """Tạo 1 ngày với 2-5 activities random."""
    is_weekend = date_obj.weekday() >= 5

    # Cuối tuần thì ít meeting hơn, nhiều event hơn
    if is_weekend:
        num_meetings = random.randint(0, 1)
        num_events = random.randint(2, 4)
    else:
        num_meetings = random.randint(1, 3)
        num_events = random.randint(1, 3)

    activities = []
    for _ in range(num_meetings):
        activities.append(random_meeting())
    for _ in range(num_events):
        activities.append(random_event())

    # Shuffle để xen kẽ meeting/event
    random.shuffle(activities)

    return {
        "date": date_obj.strftime("%d/%m/%Y"),
        "activities": activities,
    }


def main():
    random.seed(42)  # cho dữ liệu ổn định, dễ test
    schedule = []

    for i in range(NUM_DAYS):
        date_obj = TODAY + timedelta(days=i)
        schedule.append(generate_day(date_obj))

    output = {"schedule": schedule}

    with open("Data_Calendar.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Generated {NUM_DAYS} days from {TODAY.strftime('%d/%m/%Y')}")
    print(f"Total activities: {sum(len(d['activities']) for d in schedule)}")
    print(f"Saved to Data_Calendar.json")


if __name__ == "__main__":
    main()