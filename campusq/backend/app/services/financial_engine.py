from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models import (
    Payment, StudentFinancialAccount, SemesterPaymentPolicy, 
    PaymentMilestone, LatePaymentCharge, Student, Semester, AuditLog
)


def get_verified_payments(db: Session, student_id, semester_id) -> Decimal:
    """Get total verified payments for a student in a semester."""
    result = db.query(
        func.sum(Payment.amount.cast(float))
    ).filter(
        Payment.student_id == student_id,
        Payment.semester_id == semester_id,
        Payment.status == 'verified'
    ).scalar()
    
    return Decimal(str(result or 0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_pending_payments(db: Session, student_id, semester_id) -> Decimal:
    """Get total pending payments for a student in a semester."""
    result = db.query(
        func.sum(Payment.amount.cast(float))
    ).filter(
        Payment.student_id == student_id,
        Payment.semester_id == semester_id,
        Payment.status == 'pending'
    ).scalar()
    
    return Decimal(str(result or 0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_payment_percentage(verified_payments: Decimal, assessed_tuition: Decimal) -> Decimal:
    """Calculate payment percentage."""
    if assessed_tuition <= 0:
        return Decimal('0')
    
    percentage = (verified_payments / assessed_tuition) * 100
    return percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_assessed_tuition(db: Session, student_id, semester_id) -> Decimal:
    """Get assessed tuition for a student in a semester."""
    account = db.query(StudentFinancialAccount).filter(
        StudentFinancialAccount.student_id == student_id,
        StudentFinancialAccount.semester_id == semester_id
    ).first()
    
    if account:
        return Decimal(account.assessed_tuition).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return Decimal('0')


def get_semester_policy(db: Session, semester_id) -> Optional[SemesterPaymentPolicy]:
    """Get payment policy for a semester."""
    return db.query(SemesterPaymentPolicy).filter(
        SemesterPaymentPolicy.semester_id == semester_id,
        SemesterPaymentPolicy.is_active == True
    ).first()


def evaluate_milestones(
    payment_percentage: Decimal,
    policy: SemesterPaymentPolicy
) -> dict:
    """Evaluate which milestones have been achieved."""
    initial_pct = Decimal(str(policy.initial_percentage))
    second_pct = Decimal(str(policy.second_percentage))
    final_pct = Decimal(str(policy.final_percentage))
    
    return {
        'initial': {
            'percentage': initial_pct,
            'achieved': payment_percentage >= initial_pct
        },
        'second': {
            'percentage': second_pct,
            'achieved': payment_percentage >= second_pct
        },
        'final': {
            'percentage': final_pct,
            'achieved': payment_percentage >= final_pct
        }
    }


def calculate_outstanding_balance(
    assessed_tuition: Decimal,
    verified_payments: Decimal
) -> Decimal:
    """Calculate outstanding balance."""
    balance = assessed_tuition - verified_payments
    return max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_amount_for_milestone(
    milestone_percentage: Decimal,
    assessed_tuition: Decimal,
    verified_payments: Decimal
) -> Decimal:
    """Calculate amount required to reach a milestone."""
    required_amount = (milestone_percentage / 100) * assessed_tuition
    additional_required = required_amount - verified_payments
    return max(additional_required, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def check_registration_eligibility(
    payment_percentage: Decimal,
    policy: Optional[SemesterPaymentPolicy],
    other_requirements_met: bool = True
) -> tuple[bool, str]:
    """Check if student is eligible for registration based on payment percentage."""
    if not policy:
        return False, "No active payment policy found for this semester"
    
    initial_pct = Decimal(str(policy.initial_percentage))
    
    if payment_percentage < initial_pct:
        return False, f"Payment percentage ({payment_percentage}%) is below the required {initial_pct}%"
    
    if not other_requirements_met:
        return False, "Other registration requirements not met"
    
    return True, "Eligible for registration"


def get_financial_status(db: Session, student_id, semester_id) -> dict:
    """Get complete financial status for a student."""
    # Get assessed tuition
    assessed_tuition = get_assessed_tuition(db, student_id, semester_id)
    
    # Get payments
    verified_payments = get_verified_payments(db, student_id, semester_id)
    pending_payments = get_pending_payments(db, student_id, semester_id)
    
    # Calculate percentage
    payment_percentage = calculate_payment_percentage(verified_payments, assessed_tuition)
    
    # Get policy
    policy = get_semester_policy(db, semester_id)
    
    # Evaluate milestones
    milestones = {}
    registration_eligible = False
    
    if policy:
        milestones = evaluate_milestones(payment_percentage, policy)
        registration_eligible, _ = check_registration_eligibility(payment_percentage, policy)
    
    # Calculate outstanding balance
    outstanding_balance = calculate_outstanding_balance(assessed_tuition, verified_payments)
    
    # Get late charges
    late_charges = get_total_late_charges(db, student_id, semester_id)
    
    return {
        'student_id': student_id,
        'semester_id': semester_id,
        'assessed_tuition': assessed_tuition,
        'verified_payments': verified_payments,
        'pending_payments': pending_payments,
        'outstanding_balance': outstanding_balance,
        'payment_percentage': payment_percentage,
        'initial_milestone_achieved': milestones.get('initial', {}).get('achieved', False),
        'second_milestone_achieved': milestones.get('second', {}).get('achieved', False),
        'final_milestone_achieved': milestones.get('final', {}).get('achieved', False),
        'registration_eligible': registration_eligible,
        'late_charges': late_charges,
        'milestones': milestones
    }


def get_total_late_charges(db: Session, student_id, semester_id) -> Decimal:
    """Get total late charges for a student in a semester."""
    result = db.query(
        func.sum(LatePaymentCharge.amount.cast(float))
    ).filter(
        LatePaymentCharge.student_id == student_id,
        LatePaymentCharge.semester_id == semester_id,
        LatePaymentCharge.status != 'cancelled'
    ).scalar()
    
    return Decimal(str(result or 0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
