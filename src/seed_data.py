"""
Seed script to populate the database with initial data
Run this script to migrate from in-memory data to the database
"""
from database import SessionLocal, init_db
from models import Activity, Student, Membership, MembershipStatus


def seed_activities():
    """Populate activities table with initial data"""
    db = SessionLocal()
    
    try:
        # Check if activities already exist
        existing_count = db.query(Activity).count()
        if existing_count > 0:
            print(f"Activities already exist ({existing_count} found). Skipping activity seeding.")
            return
        
        activities_data = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30
            },
            {
                "name": "Soccer Team",
                "description": "Join the school soccer team and compete in matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 22
            },
            {
                "name": "Basketball Team",
                "description": "Practice and play basketball with the school team",
                "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 15
            },
            {
                "name": "Art Club",
                "description": "Explore your creativity through painting and drawing",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 15
            },
            {
                "name": "Drama Club",
                "description": "Act, direct, and produce plays and performances",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 20
            },
            {
                "name": "Math Club",
                "description": "Solve challenging problems and participate in math competitions",
                "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                "max_participants": 10
            },
            {
                "name": "Debate Team",
                "description": "Develop public speaking and argumentation skills",
                "schedule": "Fridays, 4:00 PM - 5:30 PM",
                "max_participants": 12
            },
            {
                "name": "GitHub Skills",
                "description": "Learn practical coding and collaboration skills with GitHub. Part of the GitHub Certifications program to help with college applications",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 25
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
        
        db.commit()
        print(f"Successfully seeded {len(activities_data)} activities!")
        
    except Exception as e:
        print(f"Error seeding activities: {e}")
        db.rollback()
    finally:
        db.close()


def seed_students_and_memberships():
    """Populate students and memberships with initial data"""
    db = SessionLocal()
    
    try:
        # Check if students already exist
        existing_count = db.query(Student).count()
        if existing_count > 0:
            print(f"Students already exist ({existing_count} found). Skipping student seeding.")
            return
        
        # Student data with their activity memberships
        students_data = [
            ("michael@mergington.edu", ["Chess Club"]),
            ("daniel@mergington.edu", ["Chess Club"]),
            ("emma@mergington.edu", ["Programming Class"]),
            ("sophia@mergington.edu", ["Programming Class"]),
            ("john@mergington.edu", ["Gym Class"]),
            ("olivia@mergington.edu", ["Gym Class"]),
            ("liam@mergington.edu", ["Soccer Team"]),
            ("noah@mergington.edu", ["Soccer Team"]),
            ("ava@mergington.edu", ["Basketball Team"]),
            ("mia@mergington.edu", ["Basketball Team"]),
            ("amelia@mergington.edu", ["Art Club"]),
            ("harper@mergington.edu", ["Art Club"]),
            ("ella@mergington.edu", ["Drama Club"]),
            ("scarlett@mergington.edu", ["Drama Club"]),
            ("james@mergington.edu", ["Math Club"]),
            ("benjamin@mergington.edu", ["Math Club"]),
            ("charlotte@mergington.edu", ["Debate Team"]),
            ("henry@mergington.edu", ["Debate Team"])
        ]
        
        student_count = 0
        membership_count = 0
        
        for email, activity_names in students_data:
            # Create student (basic record for now)
            student = Student(
                first_name="Pending",
                last_name="Pending",
                email=email
            )
            db.add(student)
            db.flush()  # Get student.id without committing
            student_count += 1
            
            # Create memberships
            for activity_name in activity_names:
                activity = db.query(Activity).filter(Activity.name == activity_name).first()
                if activity:
                    membership = Membership(
                        student_id=student.id,
                        activity_id=activity.id,
                        status=MembershipStatus.ACCEPTED
                    )
                    db.add(membership)
                    membership_count += 1
        
        db.commit()
        print(f"Successfully seeded {student_count} students and {membership_count} memberships!")
        
    except Exception as e:
        print(f"Error seeding students and memberships: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main function to run all seed operations"""
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    print("\nSeeding activities...")
    seed_activities()
    
    print("\nSeeding students and memberships...")
    seed_students_and_memberships()
    
    print("\n✅ Database seeding complete!")


if __name__ == "__main__":
    main()
