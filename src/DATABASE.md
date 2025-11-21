# Database Integration

This directory contains the database implementation for the Mergington High School Management System.

## Overview

The application has been migrated from in-memory storage to persistent database storage using SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL for production).

## Database Schema

### Tables

1. **students** - Student information
   - id (primary key)
   - first_name, last_name
   - email (unique)
   - password_hash (for future authentication)
   - roll_number (unique)
   - grade, phone, profile_photo_url
   - created_at, updated_at

2. **admins** - Administrator/Teacher accounts
   - id (primary key)
   - email (unique)
   - password_hash
   - name
   - created_at

3. **activities** - Clubs and activities
   - id (primary key)
   - name (unique)
   - description
   - schedule
   - max_participants
   - image_url
   - created_at, updated_at

4. **memberships** - Student-Activity relationships
   - id (primary key)
   - student_id (foreign key → students)
   - activity_id (foreign key → activities)
   - status (pending/accepted/declined)
   - created_at, updated_at

5. **events** - School events
   - id (primary key)
   - name, description
   - event_date, location
   - max_participants, registration_deadline
   - image_url
   - created_at, updated_at

6. **event_registrations** - Event registration relationships
   - id (primary key)
   - student_id (foreign key → students)
   - event_id (foreign key → events)
   - created_at

## Files

- `database.py` - Database configuration and session management
- `models.py` - SQLAlchemy models for all tables
- `seed_data.py` - Script to populate database with initial data
- `app.py` - Updated FastAPI application using database

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize and Seed Database

```bash
cd src
python seed_data.py
```

This will:
- Create the database file (`school_activities.db`)
- Create all tables
- Populate with initial activities and student data

### 3. Run the Application

```bash
cd src
uvicorn app:app --reload
```

The application will be available at http://localhost:8000

## Environment Configuration

You can configure the database URL using the `DATABASE_URL` environment variable:

```bash
# SQLite (default)
export DATABASE_URL="sqlite:///./school_activities.db"

# PostgreSQL (for production)
export DATABASE_URL="postgresql://user:password@localhost/school_db"
```

## Migration from In-Memory Storage

The seed script (`seed_data.py`) migrates all existing data:

✅ All 10 activities (Chess Club, Programming Class, etc.)
✅ All student registrations with their memberships
✅ Maintains activity capacity limits
✅ Preserves all existing functionality

## API Changes

The API endpoints remain the same, but now use persistent database storage:

- `GET /activities` - Returns all activities with participants (from database)
- `POST /activities/{activity_name}/signup` - Creates student and membership records
- `DELETE /activities/{activity_name}/unregister` - Removes membership record

## Future Enhancements

This database foundation enables:
- ✅ Authentication system (Issue #8)
- ✅ Admin dashboard with approval workflow (Issue #10)
- ✅ Events management (Issue #11)
- ✅ Student profiles (Issue #14)
- ✅ And all other planned features

## Database Migrations (Alembic)

For future schema changes, use Alembic:

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Notes

- The database file is created automatically on first run
- Student records are created with minimal info (just email) for backward compatibility
- Full student profiles will be added when authentication is implemented (Issue #8)
- Membership status is auto-approved for now; admin approval workflow coming in Issue #10
