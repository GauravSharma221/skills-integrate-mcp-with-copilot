"""
Database models for the school activities management system
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

try:
    # Try relative import first (when running as a module)
    from .database import Base
except ImportError:
    # Fall back to absolute import (when running directly from src/)
    from database import Base


class Student(Base):
    """Student model"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Will be used in authentication
    roll_number = Column(String(50), unique=True, nullable=True)
    grade = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    profile_photo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    memberships = relationship("Membership", back_populates="student", cascade="all, delete-orphan")
    event_registrations = relationship("EventRegistration", back_populates="student", cascade="all, delete-orphan")


class Admin(Base):
    """Admin/Teacher model"""
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Activity(Base):
    """Activity/Club model"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    schedule = Column(String(200), nullable=False)
    max_participants = Column(Integer, nullable=False, default=20)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    memberships = relationship("Membership", back_populates="activity", cascade="all, delete-orphan")


class MembershipStatus(str, enum.Enum):
    """Membership status enumeration"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class Membership(Base):
    """Student-Activity membership relationship"""
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    status = Column(SQLEnum(MembershipStatus), default=MembershipStatus.ACCEPTED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="memberships")
    activity = relationship("Activity", back_populates="memberships")


class Event(Base):
    """Events model"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    max_participants = Column(Integer, nullable=True)
    registration_deadline = Column(DateTime, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")


class EventRegistration(Base):
    """Event registration relationship"""
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="event_registrations")
    event = relationship("Event", back_populates="registrations")
