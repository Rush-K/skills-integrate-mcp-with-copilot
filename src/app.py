"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "Academic",
        "tags": ["Strategy", "Competition"],
        "leader": "Mr. Patel"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "STEM",
        "tags": ["Coding", "Robotics"],
        "leader": "Mrs. Johnson"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "Athletics",
        "tags": ["Fitness", "Teamwork"],
        "leader": "Coach Rivera"
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "category": "Athletics",
        "tags": ["Soccer", "Competition"],
        "leader": "Coach Bennett"
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "category": "Athletics",
        "tags": ["Basketball", "Training"],
        "leader": "Coach Simmons"
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "category": "Arts",
        "tags": ["Drawing", "Creativity"],
        "leader": "Ms. Wilson"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "category": "Arts",
        "tags": ["Performing", "Theater"],
        "leader": "Mr. Lee"
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "category": "STEM",
        "tags": ["Math", "Problem Solving"],
        "leader": "Dr. Nguyen"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "category": "Academic",
        "tags": ["Public Speaking", "Leadership"],
        "leader": "Ms. Carter"
    }
}


def build_club_profile(activity_name: str, details: dict):
    """Normalize activity data into a club directory entry."""
    return {
        "name": activity_name,
        "description": details["description"],
        "schedule": details["schedule"],
        "category": details.get("category", "General"),
        "tags": details.get("tags", []),
        "leader": details.get("leader", "Club Advisor"),
        "max_participants": details["max_participants"],
        "participants": details.get("participants", []),
    }


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/clubs")
def get_clubs(category: str | None = None):
    """Return a searchable directory of school clubs."""
    clubs = [build_club_profile(name, details) for name, details in activities.items()]
    if category:
        clubs = [club for club in clubs if club["category"].upper() == category.upper()]
    return clubs


@app.get("/clubs/{club_name}")
def get_club(club_name: str):
    """Return the club detail page data for a specific club."""
    club_name = club_name.replace("%20", " ")
    if club_name not in activities:
        raise HTTPException(status_code=404, detail="Club not found")

    return build_club_profile(club_name, activities[club_name])


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
