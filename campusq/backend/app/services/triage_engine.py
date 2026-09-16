from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models import (
    Service, ServiceCategory, Department, Ticket, ServiceRequest,
    Student, Staff, Semester
)


class TriageResult:
    def __init__(
        self,
        outcome: str,  # 'digital', 'remote', 'appointment', 'virtual_queue', 'physical'
        service: Service,
        department: Optional[Department] = None,
        requires_staff: bool = False,
        auto_approvable: bool = False,
        eligibility_met: bool = True,
        reason: Optional[str] = None
    ):
        self.outcome = outcome
        self.service = service
        self.department = department
        self.requires_staff = requires_staff
        self.auto_approvable = auto_approvable
        self.eligibility_met = eligibility_met
        self.reason = reason


def triage_service_request(
    db: Session,
    student_id: str,
    service_id: str,
    request_data: Dict[str, Any]
) -> TriageResult:
    """
    Triage a service request to determine the appropriate outcome.
    
    Decision flow:
    1. Can the system complete automatically? → DIGITAL
    2. Can staff resolve remotely? → REMOTE
    3. Does it require scheduled attendance? → APPOINTMENT
    4. Otherwise → VIRTUAL_QUEUE or PHYSICAL
    """
    # Get the service
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return TriageResult(
            outcome='physical',
            service=None,
            reason="Service not found"
        )
    
    # Check eligibility requirements
    eligibility_met, reason = check_service_eligibility(
        db, student_id, service, request_data
    )
    
    if not eligibility_met:
        return TriageResult(
            outcome='physical',
            service=service,
            eligibility_met=False,
            reason=reason
        )
    
    # Determine outcome based on service configuration
    if service.auto_approvable:
        return TriageResult(
            outcome='digital',
            service=service,
            auto_approvable=True,
            requires_staff=False
        )
    
    if service.requires_appointment:
        return TriageResult(
            outcome='appointment',
            service=service,
            requires_staff=True,
            department=get_responsible_department(db, service)
        )
    
    if service.requires_physical_visit:
        return TriageResult(
            outcome='physical',
            service=service,
            requires_staff=True,
            department=get_responsible_department(db, service)
        )
    
    # Default to remote resolution if possible
    if service.default_outcome == 'remote':
        return TriageResult(
            outcome='remote',
            service=service,
            requires_staff=True,
            department=get_responsible_department(db, service)
        )
    
    # Fallback to virtual queue
    return TriageResult(
        outcome='virtual_queue',
        service=service,
        requires_staff=True,
        department=get_responsible_department(db, service)
    )


def check_service_eligibility(
    db: Session,
    student_id: str,
    service: Service,
    request_data: Dict[str, Any]
) -> tuple[bool, Optional[str]]:
    """Check if student meets eligibility requirements for a service."""
    # Get student
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return False, "Student not found"
    
    # Parse eligibility requirements from JSONB
    requirements = service.eligibility_requirements or []
    
    for requirement in requirements:
        req_type = requirement.get('type')
        
        if req_type == 'financial_threshold':
            # Check payment percentage requirement
            min_percentage = requirement.get('min_percentage', 0)
            semester_id = request_data.get('semester_id')
            
            if semester_id:
                from app.services.financial_engine import get_financial_status
                status = get_financial_status(db, student_id, semester_id)
                
                if status['payment_percentage'] < min_percentage:
                    return False, f"Payment percentage {status['payment_percentage']}% below required {min_percentage}%"
        
        elif req_type == 'semester_registration':
            # Check if student is registered for current semester
            current_semester = db.query(Semester).filter(
                Semester.is_active == True
            ).first()
            
            if current_semester:
                from app.models import StudentSemester
                registration = db.query(StudentSemester).filter(
                    StudentSemester.student_id == student_id,
                    StudentSemester.semester_id == current_semester.id
                ).first()
                
                if not registration:
                    return False, "Student must be registered for current semester"
        
        elif req_type == 'year_of_study':
            min_year = requirement.get('min_year', 1)
            if student.year_of_study and student.year_of_study < min_year:
                return False, f"Service requires minimum year of study: {min_year}"
    
    return True, None


def get_responsible_department(
    db: Session,
    service: Service
) -> Optional[Department]:
    """Get the department responsible for a service."""
    if service.responsible_department_id:
        return db.query(Department).filter(
            Department.id == service.responsible_department_id
        ).first()
    
    if service.category_id:
        category = db.query(ServiceCategory).filter(
            ServiceCategory.id == service.category_id
        ).first()
        
        if category and category.department_id:
            return db.query(Department).filter(
                Department.id == category.department_id
            ).first()
    
    return None


def route_ticket_to_staff(
    db: Session,
    ticket: Ticket,
    department: Optional[Department] = None
) -> Optional[Staff]:
    """Route a ticket to an available staff member."""
    if not department:
        return None
    
    # Find staff in department with lowest workload
    from sqlalchemy import func
    from app.models import Staff, User
    
    staff_query = db.query(Staff).join(User).filter(
        Staff.department_id == department.id,
        Staff.deleted_at == None,
        User.status == 'active'
    )
    
    # Count active tickets per staff
    from app.models import Ticket as TicketModel
    workload = db.query(
        TicketModel.assigned_to,
        func.count(TicketModel.id).label('ticket_count')
    ).filter(
        TicketModel.status.in_(['waiting', 'in_progress', 'pending_staff'])
    ).group_by(TicketModel.assigned_to).subquery()
    
    staff_with_workload = staff_query.outerjoin(
        workload, Staff.user_id == workload.c.assigned_to
    ).order_by(
        func.coalesce(workload.c.ticket_count, 0).asc()
    ).first()
    
    return staff_with_workload
