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
    "チェスクラブ": {
        "description": "戦略を学び、チェストーナメントで競い合う",
        "schedule": "金曜日、3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "プログラミングクラス": {
        "description": "プログラミングの基礎を学び、ソフトウェアプロジェクトを構築する",
        "schedule": "火曜日と木曜日、3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "体育クラス": {
        "description": "体育とスポーツ活動",
        "schedule": "月曜日、水曜日、金曜日、2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "サッカーチーム": {
        "description": "一緒にトレーニングして、学校間のサッカーマッチで競い合う",
        "schedule": "月曜日と水曜日、4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "バスケットボールクラブ": {
        "description": "バスケットボールの基礎を開発し、毎週スクリメージをプレイ",
        "schedule": "火曜日と金曜日、4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "アートワークショップ": {
        "description": "描画、絵画、ミクストメディアアートプロジェクトを探索",
        "schedule": "木曜日、3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "logan@mergington.edu"]
    },
    "スクールバンド": {
        "description": "楽器の練習と学校行事でのパフォーマンス",
        "schedule": "水曜日、3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["ethan@mergington.edu", "amelia@mergington.edu"]
    },
    "ディベート協会": {
        "description": "正式なディベートを通じて議論スキルを構築",
        "schedule": "月曜日、3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["charlotte@mergington.edu", "james@mergington.edu"]
    },
    "数学オリンピック対策": {
        "description": "数学競技会向けの高度な問題解決を練習",
        "schedule": "金曜日、3:30 PM - 5:00 PM",
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
        raise HTTPException(status_code=404, detail="活動が見つかりません")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    normalized_email = email.strip().lower()
    normalized_participants = [p.strip().lower() for p in activity["participants"]]
    if normalized_email in normalized_participants:
        raise HTTPException(
            status_code=409,
            detail="この活動にはすでに登録されています",
        )

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"{normalized_email} が {activity_name} に登録されました"}


@app.delete("/activities/{activity_name}/remove")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="活動が見つかりません")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email
    normalized_email = email.strip().lower()
    normalized_participants = [p.strip().lower() for p in activity["participants"]]
    
    # Check if student is signed up
    if normalized_email not in normalized_participants:
        raise HTTPException(
            status_code=404,
            detail="この参加者は登録されていません",
        )

    # Remove student
    # Find the original case email and remove it
    for i, participant in enumerate(activity["participants"]):
        if participant.strip().lower() == normalized_email:
            activity["participants"].pop(i)
            break
    
    return {"message": f"{normalized_email} が {activity_name} から登録解除されました"}
