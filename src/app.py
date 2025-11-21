"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
Now with persistent database storage using SQLAlchemy.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path
from typing import List, Dict

from database import get_db, init_db
from models import Activity, Student, Membership, MembershipStatus

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)) -> Dict:
    """Get all activities with their participants"""
    activities_list = db.query(Activity).all()
    
    # Format response to match the original structure
    result = {}
    for activity in activities_list:
        # Get participant emails for accepted memberships in a single query (avoid N+1)
        participants = [
            student.email
            for student, in db.query(Student.email)
                .join(Membership, Student.id == Membership.student_id)
                .filter(
                    Membership.activity_id == activity.id,
                    Membership.status == MembershipStatus.ACCEPTED
                )
                .all()
        ]
        
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": participants
        }
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find or create student
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        # Create a basic student record with just email
        # Full profile will be added when authentication is implemented
        student = Student(
            first_name="Unknown",
            last_name="Unknown",
            email=email
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    # Check if student is already signed up (accepted membership)
    existing_membership = db.query(Membership).filter(
        Membership.student_id == student.id,
        Membership.activity_id == activity.id,
        Membership.status == MembershipStatus.ACCEPTED
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check capacity
    current_count = db.query(Membership).filter(
        Membership.activity_id == activity.id,
        Membership.status == MembershipStatus.ACCEPTED
    ).count()
    
    if current_count >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is full"
        )

    # Create membership (auto-accepted for now, will change with admin approval workflow)
    membership = Membership(
        student_id=student.id,
        activity_id=activity.id,
        status=MembershipStatus.ACCEPTED
    )
    db.add(membership)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find student
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Find membership
    membership = db.query(Membership).filter(
        Membership.student_id == student.id,
        Membership.activity_id == activity.id,
        Membership.status == MembershipStatus.ACCEPTED
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Delete membership
    db.delete(membership)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}
