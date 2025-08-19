from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import json
from ..models.course import CourseLevel, CourseStatus, EnrollmentStatus


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = None
    level: CourseLevel
    price: float = Field(..., ge=0)
    duration_hours: int = Field(..., gt=0)
    instructor_name: str = Field(..., min_length=1, max_length=100)


class CourseCreate(CourseBase):
    slug: str = Field(..., min_length=1, max_length=200)
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    instructor_bio: Optional[str] = None
    instructor_avatar_url: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = None
    level: Optional[CourseLevel] = None
    price: Optional[float] = Field(None, ge=0)
    duration_hours: Optional[int] = Field(None, gt=0)
    instructor_name: Optional[str] = Field(None, min_length=1, max_length=100)
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    instructor_bio: Optional[str] = None
    instructor_avatar_url: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    status: Optional[CourseStatus] = None
    is_featured: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    slug: str
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    status: CourseStatus
    instructor_bio: Optional[str] = None
    instructor_avatar_url: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_featured: bool
    enrollment_count: int
    rating: float
    rating_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @field_validator('learning_objectives', 'prerequisites', 'tags', mode='before')
    @classmethod
    def parse_json_string(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v or []

    class Config:
        from_attributes = True


class CourseEnrollmentCreate(BaseModel):
    course_id: int


class CourseEnrollmentResponse(BaseModel):
    id: int
    course_id: int
    status: EnrollmentStatus
    progress_percentage: float
    enrollment_date: datetime
    completion_date: Optional[datetime] = None
    certificate_url: Optional[str] = None
    course: CourseResponse

    class Config:
        from_attributes = True


class CourseProgressUpdate(BaseModel):
    lesson_id: str
    lesson_title: str
    completed: bool = False
    time_spent_minutes: int = 0
    quiz_score: Optional[float] = None
    notes: Optional[str] = None