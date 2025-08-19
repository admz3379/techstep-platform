from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate
from ...api.deps import get_current_active_user, get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get all users (admin only)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID
    """
    # Users can only get their own profile unless they're admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update user profile
    """
    # Users can only update their own profile unless they're admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete user (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Don't allow deleting self
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.get("/profile/dashboard")
def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user dashboard data
    """
    # Get user's course enrollments
    from ...models.course import CourseEnrollment, Course
    from ...models.mentor import MentorBooking
    from ...models.payment import Payment
    
    enrollments = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id
    ).join(Course).all()
    
    bookings = db.query(MentorBooking).filter(
        MentorBooking.user_id == current_user.id
    ).all()
    
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).all()
    
    return {
        "user": UserResponse.from_orm(current_user),
        "stats": {
            "total_courses": len(enrollments),
            "completed_courses": len([e for e in enrollments if e.status == "completed"]),
            "total_bookings": len(bookings),
            "completed_sessions": len([b for b in bookings if b.status == "completed"]),
            "total_spent": sum([p.amount for p in payments if p.status == "completed"])
        },
        "recent_courses": [
            {
                "id": e.course.id,
                "title": e.course.title,
                "progress": e.progress_percentage,
                "status": e.status
            } for e in enrollments[:5]
        ],
        "upcoming_sessions": [
            {
                "id": b.id,
                "title": b.session_title,
                "date": b.scheduled_date,
                "mentor": b.mentor.user.full_name if hasattr(b, 'mentor') else None
            } for b in bookings if b.status == "confirmed"
        ][:5]
    }