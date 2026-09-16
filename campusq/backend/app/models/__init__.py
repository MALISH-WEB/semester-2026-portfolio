from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    status = Column(String(20), default='active')
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    roles = relationship("UserRole", back_populates="user")
    student = relationship("Student", back_populates="user", uselist=False)
    staff = relationship("Staff", back_populates="user", uselist=False)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), default=func.now())
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="roles")
    role = relationship("Role")


class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    level = Column(String(50))
    duration_years = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"))
    year_of_study = Column(Integer)
    enrollment_year = Column(Integer)
    current_semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="student")
    payments = relationship("Payment", back_populates="student")
    financial_accounts = relationship("StudentFinancialAccount", back_populates="student")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    staff_number = Column(String(20), unique=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    position = Column(String(100))
    employee_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="staff")


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(50), nullable=False)
    academic_year = Column(String(9), nullable=False)
    semester_type = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start_date = Column(DateTime)
    registration_end_date = Column(DateTime)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class StudentSemester(Base):
    __tablename__ = "student_semesters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"))
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="CASCADE"))
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"))
    year_of_study = Column(Integer)
    is_current = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('student_id', 'semester_id'),
    )


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("service_categories.id"))
    description = Column(Text)
    responsible_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    default_outcome = Column(String(50), default='remote')
    requires_appointment = Column(Boolean, default=False)
    requires_physical_visit = Column(Boolean, default=False)
    auto_approvable = Column(Boolean, default=False)
    eligibility_requirements = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"))
    transaction_reference = Column(String(100), unique=True, nullable=False, index=True)
    amount = Column(String(20), nullable=False)  # Store as string to preserve precision
    payment_date = Column(DateTime(timezone=True), nullable=False)
    payment_method = Column(String(50))
    description = Column(Text)
    status = Column(String(20), default='pending', index=True)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    rejected_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    rejected_at = Column(DateTime(timezone=True))
    payment_metadata = Column(JSONB, default={})  # Renamed from metadata
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="payments")


class StudentFinancialAccount(Base):
    __tablename__ = "student_financial_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"))
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"))
    assessed_tuition = Column(String(20), nullable=False, default="0.00")
    currency = Column(String(3), default='UGX')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('student_id', 'semester_id'),
    )

    student = relationship("Student", back_populates="financial_accounts")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    ticket_number = Column(String(50), unique=True, nullable=False)
    service_request_id = Column(UUID(as_uuid=True), ForeignKey("service_requests.id"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    category = Column(String(100))
    description = Column(Text)
    priority = Column(String(20), default='normal')
    status = Column(String(50), default='waiting', index=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    queue_id = Column(UUID(as_uuid=True))
    expected_resolution_time = Column(String(20))
    actual_resolution_time = Column(String(20))
    resolution_notes = Column(Text)
    escalation_level = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), index=True)
    previous_value = Column(JSONB)
    new_value = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)


class SemesterPaymentPolicy(Base):
    __tablename__ = "semester_payment_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="CASCADE"), unique=True)
    initial_percentage = Column(String(5), nullable=False, default="45.00")
    second_percentage = Column(String(5), nullable=False, default="75.00")
    final_percentage = Column(String(5), nullable=False, default="100.00")
    second_deadline = Column(DateTime)
    final_deadline = Column(DateTime)
    late_payment_charge = Column(String(20), nullable=False, default="50000.00")
    currency = Column(String(3), default='UGX')
    charge_frequency = Column(String(50), default='once_per_milestone')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class PaymentMilestone(Base):
    __tablename__ = "payment_milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    policy_id = Column(UUID(as_uuid=True), ForeignKey("semester_payment_policies.id", ondelete="CASCADE"))
    milestone_order = Column(Integer, nullable=False)
    percentage = Column(String(5), nullable=False)
    deadline = Column(DateTime)
    charge_applicable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    __table_args__ = (
        UniqueConstraint('policy_id', 'milestone_order'),
    )


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    request_number = Column(String(50), unique=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"))
    category = Column(String(50))
    description = Column(Text, nullable=False)
    priority = Column(String(20), default='normal')
    outcome = Column(String(50))
    status = Column(String(50), default='submitted', index=True)
    submitted_at = Column(DateTime(timezone=True), default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class LatePaymentCharge(Base):
    __tablename__ = "late_payment_charges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"))
    payment_milestone_id = Column(UUID(as_uuid=True), ForeignKey("payment_milestones.id"))
    amount = Column(String(20), nullable=False)
    charge_date = Column(DateTime(timezone=True), default=func.now())
    reason = Column(Text)
    status = Column(String(20), default='assessed', index=True)  # assessed, waived, cancelled
    waived_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    waived_at = Column(DateTime(timezone=True))
    waiver_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())

    __table_args__ = (
        UniqueConstraint('student_id', 'semester_id', 'payment_milestone_id'),
    )


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    receipt_number = Column(String(50), unique=True, nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), index=True)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"))
    amount = Column(String(20), nullable=False)
    receipt_date = Column(DateTime(timezone=True), default=func.now())
    status = Column(String(20), default='issued')
    issued_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    notification_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    channel = Column(String(20), default='in_app')  # in_app, email, sms
    sent_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=func.now())


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    appointment_number = Column(String(50), unique=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), index=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    consultation_id = Column(UUID(as_uuid=True))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=30)
    mode = Column(String(20), default='physical')  # physical, virtual
    location = Column(String(200))
    status = Column(String(20), default='scheduled', index=True)
    notes = Column(Text)
    cancellation_reason = Column(Text)
    rescheduled_from = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    consultation_number = Column(String(50), unique=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"))
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), default=func.now())
    resolved_at = Column(DateTime(timezone=True))


class Queue(Base):
    __tablename__ = "queues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    service_category_id = Column(UUID(as_uuid=True), ForeignKey("service_categories.id"))
    is_active = Column(Boolean, default=True)
    max_capacity = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.now())


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id"), index=True)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    position = Column(Integer)
    status = Column(String(20), default='waiting')  # waiting, called, serving, completed, abandoned
    entered_at = Column(DateTime(timezone=True), default=func.now())
    called_at = Column(DateTime(timezone=True))
    served_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    counter_id = Column(UUID(as_uuid=True))


class Counter(Base):
    __tablename__ = "counters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), index=True)
    previous_status = Column(String(50))
    new_status = Column(String(50), nullable=False)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    changed_at = Column(DateTime(timezone=True), default=func.now())
    notes = Column(Text)


class TicketAssignment(Base):
    __tablename__ = "ticket_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"), index=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone=True), default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    document_type = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    related_entity_type = Column(String(50))
    related_entity_id = Column(UUID(as_uuid=True))
    uploaded_at = Column(DateTime(timezone=True), default=func.now())
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"))
    service_request_id = Column(UUID(as_uuid=True), ForeignKey("service_requests.id"))
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))
    rating = Column(Integer)
    comment = Column(Text)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=func.now())
