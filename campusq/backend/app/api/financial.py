from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List
from app.db.database import get_db
from app.models import Student, Payment, Semester
from app.schemas import FinancialStatus, RegistrationEligibilityResponse
from app.services.financial_engine import (
    get_financial_status,
    check_registration_eligibility,
    get_semester_policy,
    calculate_amount_for_milestone
)

router = APIRouter(prefix="/api/financial", tags=["Financial"])


@router.get("/students/{student_id}/status", response_model=FinancialStatus)
def get_student_financial_status(
    student_id: str,
    semester_id: str = None,
    db: Session = Depends(get_db)
):
    """Get financial status for a student."""
    # Get current or specified semester
    if not semester_id:
        current_semester = db.query(Semester).filter(
            Semester.is_active == True
        ).first()
        if not current_semester:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active semester found"
            )
        semester_id = str(current_semester.id)
    
    # Get financial status
    financial_status = get_financial_status(db, student_id, semester_id)
    
    return financial_status


@router.get("/students/{student_id}/registration-eligibility", response_model=RegistrationEligibilityResponse)
def check_student_registration_eligibility(
    student_id: str,
    semester_id: str = None,
    db: Session = Depends(get_db)
):
    """Check if a student is eligible for registration."""
    # Get current or specified semester
    if not semester_id:
        current_semester = db.query(Semester).filter(
            Semester.is_active == True
        ).first()
        if not current_semester:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active semester found"
            )
        semester_id = str(current_semester.id)
    
    # Get financial status
    financial_status = get_financial_status(db, student_id, semester_id)
    
    # Get policy
    policy = get_semester_policy(db, semester_id)
    
    if not policy:
        return RegistrationEligibilityResponse(
            eligible=False,
            reason="No active payment policy found for this semester",
            current_payment_percentage=financial_status['payment_percentage'],
            required_percentage=Decimal('45.00'),
            assessed_tuition=financial_status['assessed_tuition'],
            verified_payments=financial_status['verified_payments'],
            additional_amount_required=Decimal('0'),
            milestones={}
        )
    
    initial_pct = Decimal(str(policy.initial_percentage))
    
    # Calculate additional amount required if not eligible
    additional_required = Decimal('0')
    if financial_status['payment_percentage'] < initial_pct:
        additional_required = calculate_amount_for_milestone(
            initial_pct,
            financial_status['assessed_tuition'],
            financial_status['verified_payments']
        )
    
    eligible, reason = check_registration_eligibility(
        financial_status['payment_percentage'],
        policy
    )
    
    return RegistrationEligibilityResponse(
        eligible=eligible,
        reason=reason if not eligible else None,
        current_payment_percentage=financial_status['payment_percentage'],
        required_percentage=initial_pct,
        assessed_tuition=financial_status['assessed_tuition'],
        verified_payments=financial_status['verified_payments'],
        additional_amount_required=additional_required,
        milestones=financial_status['milestones']
    )
