from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from decimal import Decimal
import uuid
from app.db.database import get_db
from app.models import Payment, Student, StudentFinancialAccount, Semester, Receipt, User, AuditLog
from app.schemas import PaymentCreate, PaymentResponse, FinancialStatus
from app.core.security import get_current_user, require_role, User as AuthUser
from app.services.financial_engine import get_financial_status

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse)
def submit_payment(
    payment_data: PaymentCreate,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a new payment for verification."""
    # Get student record
    student = db.query(Student).filter(
        Student.user_id == current_user.id,
        Student.deleted_at == None
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not found"
        )
    
    # Verify student owns this payment
    if str(student.id) != str(payment_data.student_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit payments for other students"
        )
    
    # Check for duplicate transaction reference
    existing = db.query(Payment).filter(
        Payment.transaction_reference == payment_data.transaction_reference
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction reference already exists"
        )
    
    # Create payment
    payment = Payment(
        id=uuid.uuid4(),
        student_id=student.id,
        semester_id=payment_data.semester_id,
        transaction_reference=payment_data.transaction_reference,
        amount=str(payment_data.amount),
        payment_date=datetime.now(),
        payment_method=payment_data.payment_method,
        description=payment_data.description,
        status='pending',
        payment_metadata={}
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return {
        'id': str(payment.id),
        'student_id': str(payment.student_id),
        'semester_id': str(payment.semester_id),
        'transaction_reference': payment.transaction_reference,
        'amount': Decimal(payment.amount),
        'payment_date': payment.payment_date,
        'payment_method': payment.payment_method,
        'description': payment.description,
        'status': payment.status,
        'verified_at': payment.verified_at,
        'rejection_reason': payment.rejection_reason
    }


@router.get("/my", response_model=List[PaymentResponse])
def get_my_payments(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payments for current student."""
    student = db.query(Student).filter(
        Student.user_id == current_user.id,
        Student.deleted_at == None
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not found"
        )
    
    payments = db.query(Payment).filter(
        Payment.student_id == student.id
    ).order_by(Payment.payment_date.desc()).all()
    
    return [{
        'id': str(p.id),
        'student_id': str(p.student_id),
        'semester_id': str(p.semester_id),
        'transaction_reference': p.transaction_reference,
        'amount': Decimal(p.amount),
        'payment_date': p.payment_date,
        'payment_method': p.payment_method,
        'description': p.description,
        'status': p.status,
        'verified_at': p.verified_at,
        'rejection_reason': p.rejection_reason
    } for p in payments]


@router.post("/{payment_id}/verify")
def verify_payment(
    payment_id: str,
    verification_data: dict,
    current_user: AuthUser = Depends(require_role("accounts_officer")),
    db: Session = Depends(get_db)
):
    """Verify or reject a payment (Accounts Officer only)."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    if payment.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment is already {payment.status}"
        )
    
    action = verification_data.get('status')
    notes = verification_data.get('verification_notes', '')
    
    if action == 'verified':
        payment.status = 'verified'
        payment.verified_by = current_user.id
        payment.verified_at = datetime.now()
        
        # Generate receipt
        year = datetime.now().year
        count = db.query(Receipt).filter(
            Receipt.receipt_number.like(f"RCP-{year}-%")
        ).count()
        receipt_number = f"RCP-{year}-{str(count + 1).zfill(6)}"
        
        receipt = Receipt(
            id=uuid.uuid4(),
            receipt_number=receipt_number,
            payment_id=payment.id,
            student_id=payment.student_id,
            semester_id=payment.semester_id,
            amount=payment.amount,
            status='issued',
            issued_by=current_user.id
        )
        db.add(receipt)
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='payment_verified',
            entity_type='payment',
            entity_id=payment.id,
            new_value={'status': 'verified', 'amount': payment.amount}
        )
        db.add(audit)
        
    elif action == 'rejected':
        payment.status = 'rejected'
        payment.rejection_reason = notes
        payment.rejected_by = current_user.id
        payment.rejected_at = datetime.now()
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='payment_rejected',
            entity_type='payment',
            entity_id=payment.id,
            new_value={'status': 'rejected', 'reason': notes}
        )
        db.add(audit)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid action. Must be 'verified' or 'rejected'"
        )
    
    db.commit()
    
    return {"message": f"Payment {action}", "payment_id": str(payment.id)}
