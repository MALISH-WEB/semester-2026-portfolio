from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.models import Service, ServiceCategory, ServiceRequest, Student, Department
from app.schemas import ServiceRequestCreate, ServiceRequestResponse
from app.core.security import get_current_user, get_current_student, User
from app.services.triage_engine import triage_service_request, TriageResult
import uuid

router = APIRouter(prefix="/api/services", tags=["Services"])


@router.get("", response_model=List[dict])
def list_services(
    category: str = None,
    department: str = None,
    db: Session = Depends(get_db)
):
    """List available services with optional filtering."""
    query = db.query(Service).filter(Service.deleted_at == None)
    
    if category:
        category_obj = db.query(ServiceCategory).filter(
            ServiceCategory.code == category
        ).first()
        if category_obj:
            query = query.filter(Service.category_id == category_obj.id)
    
    if department:
        dept_obj = db.query(Department).filter(
            Department.code == department
        ).first()
        if dept_obj:
            query = query.filter(Service.responsible_department_id == dept_obj.id)
    
    services = query.all()
    return [{
        'id': str(s.id),
        'name': s.name,
        'code': s.code,
        'description': s.description,
        'category_id': str(s.category_id) if s.category_id else None,
        'responsible_department_id': str(s.responsible_department_id) if s.responsible_department_id else None,
        'auto_approvable': s.auto_approvable,
        'requires_appointment': s.requires_appointment,
        'requires_physical_visit': s.requires_physical_visit,
        'default_outcome': s.default_outcome
    } for s in services]


@router.get("/{service_id}", response_model=dict)
def get_service_details(
    service_id: str,
    db: Session = Depends(get_db)
):
    """Get details of a specific service."""
    service = db.query(Service).filter(
        Service.id == service_id,
        Service.deleted_at == None
    ).first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {
        'id': str(service.id),
        'name': service.name,
        'code': service.code,
        'description': service.description,
        'category_id': str(service.category_id) if service.category_id else None,
        'responsible_department_id': str(service.responsible_department_id) if service.responsible_department_id else None,
        'auto_approvable': service.auto_approvable,
        'requires_appointment': service.requires_appointment,
        'requires_physical_visit': service.requires_physical_visit,
        'default_outcome': service.default_outcome,
        'eligibility_requirements': service.eligibility_requirements or []
    }


@router.post("/requests", response_model=ServiceRequestResponse)
def create_service_request(
    request_data: ServiceRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a new service request."""
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
    
    # Verify student owns this request
    if str(student.id) != str(request_data.student_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit requests for other students"
        )
    
    # Get service
    service = db.query(Service).filter(
        Service.id == request_data.service_id,
        Service.deleted_at == None
    ).first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Perform triage
    triage_result: TriageResult = triage_service_request(
        db=db,
        student_id=request_data.student_id,
        service_id=request_data.service_id,
        request_data={'semester_id': getattr(request_data, 'semester_id', None)}
    )
    
    if not triage_result.eligibility_met:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=triage_result.reason
        )
    
    # Generate request number
    year = datetime.now().year
    count = db.query(ServiceRequest).filter(
        ServiceRequest.request_number.like(f"SRV-{year}-%")
    ).count()
    request_number = f"SRV-{year}-{str(count + 1).zfill(4)}"
    
    # Create service request
    service_request = ServiceRequest(
        id=uuid.uuid4(),
        request_number=request_number,
        student_id=student.id,
        service_id=service.id,
        description=request_data.description,
        priority=request_data.priority,
        outcome=triage_result.outcome,
        status='submitted' if triage_result.auto_approvable else 'pending',
        submitted_at=datetime.now()
    )
    
    db.add(service_request)
    db.commit()
    db.refresh(service_request)
    
    # If auto-approvable, process immediately
    if triage_result.auto_approvable:
        service_request.status = 'completed'
        service_request.resolved_at = datetime.now()
        db.commit()
    
    return {
        'id': str(service_request.id),
        'request_number': service_request.request_number,
        'student_id': str(service_request.student_id),
        'service_id': str(service_request.service_id),
        'description': service_request.description,
        'priority': service_request.priority,
        'outcome': service_request.outcome,
        'status': service_request.status,
        'submitted_at': service_request.submitted_at,
        'resolved_at': service_request.resolved_at
    }


@router.get("/requests/my", response_model=List[ServiceRequestResponse])
def get_my_service_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get service requests for current student."""
    student = db.query(Student).filter(
        Student.user_id == current_user.id,
        Student.deleted_at == None
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not found"
        )
    
    requests = db.query(ServiceRequest).filter(
        ServiceRequest.student_id == student.id
    ).order_by(ServiceRequest.submitted_at.desc()).all()
    
    return [{
        'id': str(r.id),
        'request_number': r.request_number,
        'student_id': str(r.student_id),
        'service_id': str(r.service_id),
        'description': r.description,
        'priority': r.priority,
        'outcome': r.outcome,
        'status': r.status,
        'submitted_at': r.submitted_at,
        'resolved_at': r.resolved_at
    } for r in requests]
