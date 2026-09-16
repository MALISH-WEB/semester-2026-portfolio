from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


# Auth schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[List[str]] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


# Student schemas
class StudentCreate(BaseModel):
    user_id: UUID4
    student_number: str
    program_id: Optional[UUID4] = None
    year_of_study: Optional[int] = None
    enrollment_year: Optional[int] = None


class StudentResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    student_number: str
    program_id: Optional[UUID4] = None
    year_of_study: Optional[int] = None
    enrollment_year: Optional[int] = None

    class Config:
        from_attributes = True


# Financial schemas
class PaymentCreate(BaseModel):
    student_id: UUID4
    semester_id: UUID4
    transaction_reference: str
    amount: Decimal = Field(..., ge=0)
    payment_method: Optional[str] = None
    description: Optional[str] = None


class PaymentResponse(BaseModel):
    id: UUID4
    student_id: UUID4
    semester_id: UUID4
    transaction_reference: str
    amount: Decimal
    payment_date: datetime
    payment_method: Optional[str] = None
    description: Optional[str] = None
    status: str
    verified_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentVerificationRequest(BaseModel):
    payment_id: UUID4
    status: str  # 'verified' or 'rejected'
    verification_notes: Optional[str] = None


class FinancialStatus(BaseModel):
    student_id: UUID4
    semester_id: UUID4
    assessed_tuition: Decimal
    verified_payments: Decimal
    pending_payments: Decimal
    outstanding_balance: Decimal
    payment_percentage: Decimal
    initial_milestone_achieved: bool
    second_milestone_achieved: bool
    final_milestone_achieved: bool
    registration_eligible: bool
    late_charges: Decimal
    milestones: Optional[Dict[str, Any]] = None


# Ticket schemas
class TicketCreate(BaseModel):
    student_id: UUID4
    service_request_id: Optional[UUID4] = None
    department_id: Optional[UUID4] = None
    category: Optional[str] = None
    description: str
    priority: str = "normal"


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[UUID4] = None
    resolution_notes: Optional[str] = None
    escalation_level: Optional[int] = None


class TicketResponse(BaseModel):
    id: UUID4
    ticket_number: str
    student_id: UUID4
    department_id: Optional[UUID4] = None
    category: Optional[str] = None
    description: str
    priority: str
    status: str
    assigned_to: Optional[UUID4] = None
    escalation_level: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Service schemas
class ServiceRequestCreate(BaseModel):
    student_id: UUID4
    service_id: UUID4
    description: str
    priority: str = "normal"


class ServiceRequestResponse(BaseModel):
    id: UUID4
    request_number: str
    student_id: UUID4
    service_id: UUID4
    description: str
    priority: str
    outcome: Optional[str] = None
    status: str
    submitted_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Registration eligibility
class RegistrationEligibilityResponse(BaseModel):
    eligible: bool
    reason: Optional[str] = None
    current_payment_percentage: Decimal
    required_percentage: Decimal
    assessed_tuition: Decimal
    verified_payments: Decimal
    additional_amount_required: Decimal
    milestones: dict


# Notification schemas
class NotificationResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    notification_type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Audit log schema
class AuditLogResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    action: str
    entity_type: str
    entity_id: UUID4
    previous_value: Optional[dict] = None
    new_value: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Receipt schema
class ReceiptResponse(BaseModel):
    id: UUID4
    receipt_number: str
    payment_id: UUID4
    student_id: UUID4
    semester_id: UUID4
    amount: Decimal
    receipt_date: datetime
    status: str

    class Config:
        from_attributes = True


# Appointment schemas
class AppointmentCreate(BaseModel):
    student_id: UUID4
    staff_id: Optional[UUID4] = None
    consultation_id: Optional[UUID4] = None
    department_id: Optional[UUID4] = None
    scheduled_date: datetime
    scheduled_time: datetime
    mode: str = "physical"
    location: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: UUID4
    appointment_number: str
    student_id: UUID4
    staff_id: Optional[UUID4] = None
    scheduled_date: datetime
    scheduled_time: datetime
    duration_minutes: int
    mode: str
    location: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
