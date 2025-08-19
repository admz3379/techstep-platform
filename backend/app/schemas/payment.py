from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..models.payment import PaymentStatus, PaymentMethod, PaymentType, SubscriptionStatus, SubscriptionPlan


class PaymentCreate(BaseModel):
    payment_method: PaymentMethod
    payment_type: PaymentType
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    description: Optional[str] = None
    course_id: Optional[int] = None
    mentor_booking_id: Optional[int] = None
    subscription_id: Optional[int] = None
    payment_metadata: Optional[dict] = None


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    payment_intent_id: Optional[str] = None
    receipt_url: Optional[str] = None
    refund_amount: Optional[float] = Field(None, ge=0)
    refund_reason: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    payment_intent_id: str
    payment_method: PaymentMethod
    payment_type: PaymentType
    status: PaymentStatus
    amount: float
    currency: str
    description: Optional[str] = None
    payment_metadata: Optional[dict] = None
    course_id: Optional[int] = None
    mentor_booking_id: Optional[int] = None
    subscription_id: Optional[int] = None
    transaction_fee: float
    net_amount: float
    receipt_url: Optional[str] = None
    refund_amount: float
    refund_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    plan: SubscriptionPlan
    price_per_month: float = Field(..., gt=0)
    trial_days: Optional[int] = Field(None, ge=0, le=365)


class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatus] = None
    cancel_at_period_end: Optional[bool] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    subscription_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    cancelled_at: Optional[datetime] = None
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    price_per_month: float
    discount_percentage: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StripePaymentIntentCreate(BaseModel):
    amount: int  # Amount in cents
    currency: str = "usd"
    payment_metadata: Optional[dict] = None


class PayPalOrderCreate(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    return_url: str
    cancel_url: str