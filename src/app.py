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
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Train together and compete in inter-school soccer matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Develop basketball fundamentals and play weekly scrimmages",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and mixed-media art projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "logan@mergington.edu"]
    },
    "School Band": {
        "description": "Practice instruments and perform at school events",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["ethan@mergington.edu", "amelia@mergington.edu"]
    },
    "Debate Society": {
        "description": "Build argumentation skills through formal debates",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["charlotte@mergington.edu", "james@mergington.edu"]
    },
    "Math Olympiad Prep": {
        "description": "Practice advanced problem-solving for math competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["henry@mergington.edu", "evelyn@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    normalized_email = email.strip().lower()
    normalized_participants = [p.strip().lower() for p in activity["participants"]]
    if normalized_email in normalized_participants:
        raise HTTPException(
            status_code=409,
            detail="Student already signed up for this activity",
        )

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
