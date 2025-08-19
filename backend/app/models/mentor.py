from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from ..db.database import Base


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MentorSpecialty(str, Enum):
    PENETRATION_TESTING = "penetration_testing"
    NETWORK_SECURITY = "network_security"
    WEB_SECURITY = "web_security"
    CLOUD_SECURITY = "cloud_security"
    INCIDENT_RESPONSE = "incident_response"
    COMPLIANCE = "compliance"
    THREAT_HUNTING = "threat_hunting"
    MALWARE_ANALYSIS = "malware_analysis"


class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)  # e.g., "Senior Security Consultant"
    company = Column(String, nullable=True)
    years_experience = Column(Integer, nullable=False)
    specialties = Column(Text, nullable=False)  # JSON string of specialties
    hourly_rate = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    bio = Column(Text, nullable=False)
    certifications = Column(Text, nullable=True)  # JSON string
    languages = Column(Text, nullable=True)  # JSON string
    timezone = Column(String, nullable=False)
    availability = Column(Text, nullable=True)  # JSON string of available time slots
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    linkedin_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    bookings = relationship("MentorBooking", back_populates="mentor")


class MentorBooking(Base):
    __tablename__ = "mentor_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False)
    session_title = Column(String, nullable=False)
    session_description = Column(Text, nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=60)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    meeting_url = Column(String, nullable=True)
    meeting_notes = Column(Text, nullable=True)
    mentor_feedback = Column(Text, nullable=True)
    student_feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String, default="pending")  # pending, paid, refunded
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="mentor_bookings")
    mentor = relationship("Mentor", back_populates="bookings")