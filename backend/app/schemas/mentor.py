from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.mentor import BookingStatus, MentorSpecialty


class MentorBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: Optional[str] = None
    years_experience: int = Field(..., ge=0)
    hourly_rate: float = Field(..., gt=0)
    bio: str = Field(..., min_length=1)
    timezone: str = Field(..., min_length=1)


class MentorCreate(MentorBase):
    specialties: List[str] = Field(..., min_items=1)
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    availability: Optional[dict] = None
    linkedin_url: Optional[str] = None


class MentorUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = None
    years_experience: Optional[int] = Field(None, ge=0)
    hourly_rate: Optional[float] = Field(None, gt=0)
    bio: Optional[str] = Field(None, min_length=1)
    timezone: Optional[str] = Field(None, min_length=1)
    specialties: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    availability: Optional[dict] = None
    linkedin_url: Optional[str] = None
    is_active: Optional[bool] = None


class MentorResponse(MentorBase):
    id: int
    user_id: int
    specialties: List[str]
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    availability: Optional[dict] = None
    rating: float
    rating_count: int
    total_sessions: int
    is_featured: bool
    is_active: bool
    linkedin_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # User information
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class MentorBookingCreate(BaseModel):
    mentor_id: int
    session_title: str = Field(..., min_length=1, max_length=200)
    session_description: Optional[str] = None
    scheduled_date: datetime
    duration_minutes: int = Field(60, gt=0, le=480)  # Max 8 hours


class MentorBookingUpdate(BaseModel):
    session_title: Optional[str] = Field(None, min_length=1, max_length=200)
    session_description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, gt=0, le=480)
    status: Optional[BookingStatus] = None
    meeting_url: Optional[str] = None
    meeting_notes: Optional[str] = None
    mentor_feedback: Optional[str] = None
    student_feedback: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class MentorBookingResponse(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    session_title: str
    session_description: Optional[str] = None
    scheduled_date: datetime
    duration_minutes: int
    status: BookingStatus
    meeting_url: Optional[str] = None
    meeting_notes: Optional[str] = None
    mentor_feedback: Optional[str] = None
    student_feedback: Optional[str] = None
    rating: Optional[int] = None
    total_amount: float
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related data
    mentor_name: Optional[str] = None
    student_name: Optional[str] = None

    class Config:
        from_attributes = True