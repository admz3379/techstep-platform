from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ...db.database import get_db
from ...models.user import User
from ...models.course import Course, CourseEnrollment, CourseProgress
from ...schemas.course import (
    CourseCreate, CourseResponse, CourseUpdate, 
    CourseEnrollmentCreate, CourseEnrollmentResponse,
    CourseProgressUpdate
)
from ...api.deps import get_current_active_user, get_current_admin_user
import json

router = APIRouter()


@router.get("/", response_model=List[CourseResponse])
def get_courses(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search in title and description"),
    level: Optional[str] = Query(None, description="Filter by course level"),
    featured: Optional[bool] = Query(None, description="Filter featured courses"),
    db: Session = Depends(get_db)
):
    """
    Get all published courses with optional filtering
    """
    query = db.query(Course).filter(Course.status == "published")
    
    if search:
        query = query.filter(
            or_(
                Course.title.ilike(f"%{search}%"),
                Course.description.ilike(f"%{search}%"),
                Course.instructor_name.ilike(f"%{search}%")
            )
        )
    
    if level:
        query = query.filter(Course.level == level)
    
    if featured is not None:
        query = query.filter(Course.is_featured == featured)
    
    courses = query.order_by(Course.created_at.desc()).offset(skip).limit(limit).all()
    
    return [CourseResponse.from_orm(course) for course in courses]


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Get course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Only show published courses to non-admin users
    # For now, we'll show all courses - add user role check later if needed
    return CourseResponse.from_orm(course)


@router.post("/", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new course (admin only)
    """
    # Check if slug already exists
    if db.query(Course).filter(Course.slug == course_data.slug).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this slug already exists"
        )
    
    # Convert lists to JSON strings
    course_dict = course_data.dict()
    if course_dict.get('learning_objectives'):
        course_dict['learning_objectives'] = json.dumps(course_dict['learning_objectives'])
    if course_dict.get('prerequisites'):
        course_dict['prerequisites'] = json.dumps(course_dict['prerequisites'])
    if course_dict.get('tags'):
        course_dict['tags'] = json.dumps(course_dict['tags'])
    
    course = Course(**course_dict)
    db.add(course)
    db.commit()
    db.refresh(course)
    
    return CourseResponse.from_orm(course)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update course (admin only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Update course fields
    update_data = course_update.dict(exclude_unset=True)
    
    # Convert lists to JSON strings
    if 'learning_objectives' in update_data and update_data['learning_objectives']:
        update_data['learning_objectives'] = json.dumps(update_data['learning_objectives'])
    if 'prerequisites' in update_data and update_data['prerequisites']:
        update_data['prerequisites'] = json.dumps(update_data['prerequisites'])
    if 'tags' in update_data and update_data['tags']:
        update_data['tags'] = json.dumps(update_data['tags'])
    
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    
    return CourseResponse.from_orm(course)


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete course (admin only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if course has enrollments
    enrollment_count = db.query(CourseEnrollment).filter(CourseEnrollment.course_id == course_id).count()
    if enrollment_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete course with existing enrollments"
        )
    
    db.delete(course)
    db.commit()
    
    return {"message": "Course deleted successfully"}


@router.post("/{course_id}/enroll", response_model=CourseEnrollmentResponse)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Enroll current user in a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.status != "published":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not available for enrollment"
        )
    
    # Check if user is already enrolled
    existing_enrollment = db.query(CourseEnrollment).filter(
        and_(
            CourseEnrollment.user_id == current_user.id,
            CourseEnrollment.course_id == course_id
        )
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    # Create enrollment
    enrollment = CourseEnrollment(
        user_id=current_user.id,
        course_id=course_id
    )
    
    db.add(enrollment)
    
    # Update course enrollment count
    course.enrollment_count += 1
    
    db.commit()
    db.refresh(enrollment)
    
    return CourseEnrollmentResponse.from_orm(enrollment)


@router.get("/enrollments/my", response_model=List[CourseEnrollmentResponse])
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's course enrollments
    """
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id
    ).join(Course).all()
    
    return [CourseEnrollmentResponse.from_orm(enrollment) for enrollment in enrollments]


@router.put("/enrollments/{enrollment_id}/progress")
def update_course_progress(
    enrollment_id: int,
    progress_data: CourseProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update progress for a specific lesson in an enrollment
    """
    enrollment = db.query(CourseEnrollment).filter(
        and_(
            CourseEnrollment.id == enrollment_id,
            CourseEnrollment.user_id == current_user.id
        )
    ).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Check if progress record exists for this lesson
    progress = db.query(CourseProgress).filter(
        and_(
            CourseProgress.enrollment_id == enrollment_id,
            CourseProgress.lesson_id == progress_data.lesson_id
        )
    ).first()
    
    if progress:
        # Update existing progress
        for field, value in progress_data.dict(exclude_unset=True).items():
            setattr(progress, field, value)
        
        if progress_data.completed:
            from datetime import datetime
            progress.completion_date = datetime.utcnow()
    else:
        # Create new progress record
        progress_dict = progress_data.dict()
        progress_dict['enrollment_id'] = enrollment_id
        
        if progress_data.completed:
            from datetime import datetime
            progress_dict['completion_date'] = datetime.utcnow()
            
        progress = CourseProgress(**progress_dict)
        db.add(progress)
    
    # Calculate overall progress percentage
    total_lessons = db.query(CourseProgress).filter(
        CourseProgress.enrollment_id == enrollment_id
    ).count()
    
    completed_lessons = db.query(CourseProgress).filter(
        and_(
            CourseProgress.enrollment_id == enrollment_id,
            CourseProgress.completed == True
        )
    ).count()
    
    if total_lessons > 0:
        enrollment.progress_percentage = (completed_lessons / total_lessons) * 100
        
        # Mark course as completed if 100% progress
        if enrollment.progress_percentage >= 100:
            enrollment.status = "completed"
            from datetime import datetime
            enrollment.completion_date = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Progress updated successfully", "progress_percentage": enrollment.progress_percentage}