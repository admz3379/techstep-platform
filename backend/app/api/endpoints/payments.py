from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.user import User
from ...models.course import Course
from ...models.payment import Payment, PaymentStatus, PaymentMethod, PaymentType
from ...schemas.payment import PaymentCreate, PaymentResponse
from ...core.security import get_password_hash
from ...core.config import settings
import stripe
import secrets
import string
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentIntentCreate(BaseModel):
    course_id: int
    amount: int  # Amount in cents
    currency: str = "usd"
    payment_type: str  # "self-paced" or "mentor"
    customer_info: Dict[str, Any]

class ConsultationBooking(BaseModel):
    course_id: int
    course_title: str
    first_name: str
    last_name: str
    email: str
    phone: str
    time_slot: str
    message: str = ""

@router.post("/create-intent")
def create_payment_intent(
    payment_data: PaymentIntentCreate,
    db: Session = Depends(get_db)
):
    """
    Create Stripe payment intent for course purchase
    """
    try:
        # Get course information
        course = db.query(Course).filter(Course.id == payment_data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=payment_data.amount,
            currency=payment_data.currency,
            metadata={
                'course_id': str(payment_data.course_id),
                'course_title': course.title,
                'payment_type': payment_data.payment_type,
                'customer_first_name': payment_data.customer_info.get('first_name'),
                'customer_last_name': payment_data.customer_info.get('last_name'),
                'customer_email': payment_data.customer_info.get('email'),
            }
        )

        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment intent creation failed: {str(e)}"
        )


class PaymentConfirm(BaseModel):
    payment_intent_id: str

@router.post("/confirm")
def confirm_payment(
    payment_data: PaymentConfirm,
    db: Session = Depends(get_db)
):
    """
    Confirm payment and create user account with course access
    """
    try:
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_data.payment_intent_id)
        
        if intent.status != 'succeeded':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment not completed"
            )

        metadata = intent.metadata
        
        # Check if user already exists
        user_email = metadata.get('customer_email')
        existing_user = db.query(User).filter(User.email == user_email).first()
        
        if existing_user:
            user = existing_user
        else:
            # Create new user account
            username = user_email.split('@')[0] + '_' + ''.join(secrets.choice(string.digits) for _ in range(4))
            temporary_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            
            user = User(
                email=user_email,
                username=username,
                full_name=f"{metadata.get('customer_first_name')} {metadata.get('customer_last_name')}",
                hashed_password=get_password_hash(temporary_password),
                role="student",
                is_verified=True  # Auto-verify paid users
            )
            
            db.add(user)
            db.flush()  # Flush to get user ID

        # Create payment record
        course_id = int(metadata.get('course_id'))
        payment_type_value = PaymentType.COURSE_PURCHASE
        
        payment = Payment(
            user_id=user.id,
            payment_intent_id=payment_data.payment_intent_id,
            payment_method=PaymentMethod.STRIPE,
            payment_type=payment_type_value,
            status=PaymentStatus.COMPLETED,
            amount=intent.amount / 100,  # Convert from cents
            currency=intent.currency.upper(),
            description=f"Course purchase: {metadata.get('course_title')}",
            course_id=course_id,
            transaction_fee=0.0,  # You can calculate actual Stripe fees
            net_amount=intent.amount / 100,
            processed_at=datetime.utcnow()
        )
        
        db.add(payment)

        # Auto-enroll user in the course
        from ...models.course import CourseEnrollment
        
        enrollment = CourseEnrollment(
            user_id=user.id,
            course_id=course_id,
            status="active"
        )
        
        db.add(enrollment)
        
        # Update course enrollment count
        course = db.query(Course).filter(Course.id == course_id).first()
        course.enrollment_count += 1
        
        db.commit()

        # Send email with login credentials (if new user)
        if not existing_user:
            send_welcome_email(user_email, username, temporary_password, metadata.get('course_title'))

        return {
            "message": "Payment confirmed and account created",
            "user_id": user.id,
            "enrollment_id": enrollment.id,
            "login_sent": not bool(existing_user)
        }

    except stripe.error.StripeError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment confirmation failed: {str(e)}"
        )


@router.post("/consultations/book")
def book_consultation(
    booking_data: ConsultationBooking,
    db: Session = Depends(get_db)
):
    """
    Book a free consultation
    """
    try:
        # Here you would integrate with a calendar system
        # For now, we'll just store the booking request
        
        # You can integrate with Calendly, Google Calendar, or other booking systems
        
        # Send confirmation email
        send_consultation_confirmation_email(
            booking_data.email,
            booking_data.first_name,
            booking_data.course_title,
            booking_data.time_slot
        )
        
        return {
            "message": "Consultation booked successfully",
            "booking_id": f"CONSULT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "status": "confirmed"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking failed: {str(e)}"
        )


def send_welcome_email(email: str, username: str, password: str, course_title: str):
    """
    Send welcome email with login credentials
    """
    # TODO: Implement email sending
    # You can use SendGrid, AWS SES, or SMTP
    print(f"""
    === WELCOME EMAIL ===
    To: {email}
    Subject: Welcome to TechStep - Your Login Credentials
    
    Dear Student,
    
    Thank you for purchasing "{course_title}"!
    
    Your login credentials:
    Email: {email}
    Username: {username}
    Password: {password}
    
    Login at: {settings.FRONTEND_URL}
    
    Best regards,
    TechStep Team
    =====================
    """)


def send_consultation_confirmation_email(email: str, first_name: str, course_title: str, time_slot: str):
    """
    Send consultation confirmation email
    """
    # TODO: Implement email sending and calendar integration
    print(f"""
    === CONSULTATION CONFIRMATION ===
    To: {email}
    Subject: FREE Consultation Confirmed - {course_title}
    
    Dear {first_name},
    
    Your FREE 30-minute consultation has been confirmed!
    
    Course: {course_title}
    Time: {time_slot}
    
    We'll send you a Zoom link 15 minutes before the session.
    
    Best regards,
    TechStep Team
    =================================
    """)


def generate_random_password():
    """Generate a random password for new users"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))


# NEW ENDPOINTS AS REQUESTED

class PaymentIntentRequest(BaseModel):
    amount: int  # in cents
    currency: str = "usd"
    course_id: int
    customer_name: str
    customer_email: str
    customer_phone: str

class PaymentConfirmRequest(BaseModel):
    payment_intent_id: str
    course_id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    amount: int

@router.post("/create-payment-intent")
async def create_payment_intent_new(request: PaymentIntentRequest):
    """
    Create Stripe payment intent - NEW ENDPOINT
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency=request.currency,
            metadata={
                'course_id': request.course_id,
                'customer_name': request.customer_name,
                'customer_email': request.customer_email,
                'customer_phone': request.customer_phone
            }
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/confirm-payment")
async def confirm_payment_new(request: PaymentConfirmRequest, db: Session = Depends(get_db)):
    """
    Confirm payment and create user account - NEW ENDPOINT
    """
    try:
        # Verify payment intent was successful
        intent = stripe.PaymentIntent.retrieve(request.payment_intent_id)
        
        if intent.status != 'succeeded':
            raise HTTPException(status_code=400, detail="Payment not successful")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.customer_email).first()
        
        if existing_user:
            user = existing_user
            new_user_created = False
        else:
            # Create user account automatically
            username = request.customer_email.split('@')[0] + '_' + ''.join(secrets.choice(string.digits) for _ in range(4))
            random_password = generate_random_password()
            
            user = User(
                email=request.customer_email,
                username=username,
                full_name=request.customer_name,
                phone=request.customer_phone,
                hashed_password=get_password_hash(random_password),
                role="student",
                is_verified=True  # Auto-verify paid users
            )
            
            db.add(user)
            db.flush()  # Flush to get user ID
            new_user_created = True
        
        # Create payment record
        payment = Payment(
            user_id=user.id,
            payment_intent_id=request.payment_intent_id,
            payment_method=PaymentMethod.STRIPE,
            payment_type=PaymentType.COURSE_PURCHASE,
            status=PaymentStatus.COMPLETED,
            amount=request.amount / 100,  # Convert from cents
            currency=request.currency.upper(),
            description=f"Course purchase: Course ID {request.course_id}",
            course_id=request.course_id,
            transaction_fee=0.0,
            net_amount=request.amount / 100,
            processed_at=datetime.utcnow()
        )
        
        db.add(payment)

        # Auto-enroll user in the course
        from ...models.course import CourseEnrollment
        
        # Check if already enrolled
        existing_enrollment = db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == user.id,
            CourseEnrollment.course_id == request.course_id
        ).first()
        
        if not existing_enrollment:
            enrollment = CourseEnrollment(
                user_id=user.id,
                course_id=request.course_id,
                status="active"
            )
            db.add(enrollment)
            
            # Update course enrollment count
            course = db.query(Course).filter(Course.id == request.course_id).first()
            if course:
                course.enrollment_count += 1
        
        db.commit()

        # Send login credentials via email if new user
        if new_user_created:
            # TODO: Implement actual email sending
            print(f"""
            === LOGIN CREDENTIALS EMAIL ===
            To: {request.customer_email}
            Subject: Welcome to TechStep - Your Login Credentials
            
            Dear {request.customer_name},
            
            Welcome to TechStep! Your account has been created.
            
            Login Details:
            Email: {request.customer_email}
            Username: {user.username}
            Password: {random_password}
            
            Login at: {settings.FRONTEND_URL}
            
            Best regards,
            TechStep Team
            ===============================
            """)
        
        return {
            "status": "success", 
            "message": "Payment confirmed and account created",
            "user_id": user.id,
            "new_user": new_user_created
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all payments (admin endpoint)
    """
    payments = db.query(Payment).offset(skip).limit(limit).all()
    return [PaymentResponse.from_orm(payment) for payment in payments]