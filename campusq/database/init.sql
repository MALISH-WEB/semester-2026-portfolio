-- CampusQ Database Initialization Script
-- Uganda Christian University Digital Student Services Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');
CREATE TYPE payment_status AS ENUM ('pending', 'verified', 'rejected', 'cancelled');
CREATE TYPE ticket_status AS ENUM ('waiting', 'called', 'serving', 'in_progress', 'pending_student', 'pending_staff', 'escalated', 'resolved', 'completed', 'cancelled', 'rejected');
CREATE TYPE appointment_status AS ENUM ('scheduled', 'confirmed', 'completed', 'cancelled', 'missed', 'rescheduled');
CREATE TYPE charge_frequency AS ENUM ('once_per_milestone', 'once_per_semester', 'recurring');
CREATE TYPE service_outcome AS ENUM ('digital', 'remote', 'appointment', 'virtual_queue', 'physical');

-- Roles table
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status user_status DEFAULT 'active',
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- User roles mapping (many-to-many)
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);

-- Departments table
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES departments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Programs table
CREATE TABLE programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    department_id UUID REFERENCES departments(id),
    level VARCHAR(50), -- Undergraduate, Postgraduate, etc.
    duration_years INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Students table
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    program_id UUID REFERENCES programs(id),
    year_of_study INTEGER,
    enrollment_year INTEGER,
    current_semester_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Staff table
CREATE TABLE staff (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    staff_number VARCHAR(20) UNIQUE,
    department_id UUID REFERENCES departments(id),
    position VARCHAR(100),
    employee_type VARCHAR(50), -- Full-time, Part-time, Contract
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Semesters table
CREATE TABLE semesters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    academic_year VARCHAR(9) NOT NULL, -- e.g., "2024/2025"
    semester_type VARCHAR(20) NOT NULL, -- Regular, Recess, Special
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    registration_start_date DATE,
    registration_end_date DATE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Student semesters tracking
CREATE TABLE student_semesters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    semester_id UUID REFERENCES semesters(id) ON DELETE CASCADE,
    program_id UUID REFERENCES programs(id),
    year_of_study INTEGER,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, semester_id)
);

-- Service categories table
CREATE TABLE service_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    department_id UUID REFERENCES departments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Services table
CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    category_id UUID REFERENCES service_categories(id),
    description TEXT,
    responsible_department_id UUID REFERENCES departments(id),
    default_outcome service_outcome DEFAULT 'remote',
    requires_appointment BOOLEAN DEFAULT FALSE,
    requires_physical_visit BOOLEAN DEFAULT FALSE,
    auto_approvable BOOLEAN DEFAULT FALSE,
    eligibility_requirements JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Service requirements table
CREATE TABLE service_requirements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_id UUID REFERENCES services(id) ON DELETE CASCADE,
    requirement_type VARCHAR(50) NOT NULL, -- document, field, condition
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_required BOOLEAN DEFAULT TRUE,
    validation_rule JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Semester payment policies table
CREATE TABLE semester_payment_policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    semester_id UUID REFERENCES semesters(id) ON DELETE CASCADE,
    initial_percentage DECIMAL(5,2) NOT NULL DEFAULT 45.00,
    second_percentage DECIMAL(5,2) NOT NULL DEFAULT 75.00,
    final_percentage DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    second_deadline DATE,
    final_deadline DATE,
    late_payment_charge DECIMAL(12,2) NOT NULL DEFAULT 50000.00,
    currency VARCHAR(3) DEFAULT 'UGX',
    charge_frequency charge_frequency DEFAULT 'once_per_milestone',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(semester_id)
);

-- Payment milestones table
CREATE TABLE payment_milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID REFERENCES semester_payment_policies(id) ON DELETE CASCADE,
    milestone_order INTEGER NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    deadline DATE,
    charge_applicable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(policy_id, milestone_order)
);

-- Student financial accounts table
CREATE TABLE student_financial_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    semester_id UUID REFERENCES semesters(id) ON DELETE CASCADE,
    assessed_tuition DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'UGX',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, semester_id)
);

-- Payments table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    semester_id UUID REFERENCES semesters(id) ON DELETE CASCADE,
    transaction_reference VARCHAR(100) UNIQUE NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    payment_method VARCHAR(50),
    description TEXT,
    status payment_status DEFAULT 'pending',
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMP WITH TIME ZONE,
    rejection_reason TEXT,
    rejected_by UUID REFERENCES users(id),
    rejected_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Payment verifications audit table
CREATE TABLE payment_verifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id UUID REFERENCES payments(id) ON DELETE CASCADE,
    previous_status payment_status,
    new_status payment_status NOT NULL,
    verified_by UUID REFERENCES users(id),
    verification_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Late payment charges table
CREATE TABLE late_payment_charges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    semester_id UUID REFERENCES semesters(id) ON DELETE CASCADE,
    milestone_id UUID REFERENCES payment_milestones(id),
    charge_amount DECIMAL(12,2) NOT NULL,
    charge_reason VARCHAR(200),
    charged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    waived BOOLEAN DEFAULT FALSE,
    waived_by UUID REFERENCES users(id),
    waived_at TIMESTAMP WITH TIME ZONE,
    waiver_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, semester_id, milestone_id)
);

-- Receipts table
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    payment_id UUID REFERENCES payments(id) ON DELETE CASCADE,
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    semester_id UUID REFERENCES semesters(id),
    amount DECIMAL(12,2) NOT NULL,
    receipt_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    generated_by UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'issued',
    pdf_path VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Service requests table
CREATE TABLE service_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_number VARCHAR(50) UNIQUE NOT NULL,
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    service_id UUID REFERENCES services(id),
    category VARCHAR(50),
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal', -- low, normal, high, urgent
    outcome service_outcome,
    status VARCHAR(50) DEFAULT 'submitted',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    resolved_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    service_request_id UUID REFERENCES service_requests(id),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    department_id UUID REFERENCES departments(id),
    category VARCHAR(100),
    description TEXT,
    priority VARCHAR(20) DEFAULT 'normal',
    status ticket_status DEFAULT 'waiting',
    assigned_to UUID REFERENCES users(id),
    queue_id UUID,
    expected_resolution_time INTERVAL,
    actual_resolution_time INTERVAL,
    resolution_notes TEXT,
    escalation_level INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Ticket status history table
CREATE TABLE ticket_status_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
    previous_status ticket_status,
    new_status ticket_status NOT NULL,
    changed_by UUID REFERENCES users(id),
    change_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ticket assignments table
CREATE TABLE ticket_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES users(id),
    assigned_by UUID REFERENCES users(id),
    assignment_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Queues table
CREATE TABLE queues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    department_id UUID REFERENCES departments(id),
    service_category_id UUID REFERENCES service_categories(id),
    max_capacity INTEGER DEFAULT 50,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Queue entries table
CREATE TABLE queue_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    queue_id UUID REFERENCES queues(id) ON DELETE CASCADE,
    ticket_id UUID REFERENCES tickets(id),
    student_id UUID REFERENCES students(id),
    position INTEGER NOT NULL,
    priority INTEGER DEFAULT 0,
    estimated_wait_time INTERVAL,
    called_at TIMESTAMP WITH TIME ZONE,
    served_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    abandoned_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'waiting',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Counters table
CREATE TABLE counters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    queue_id UUID REFERENCES queues(id),
    assigned_staff_id UUID REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_type VARCHAR(50) NOT NULL, -- student, ticket, service_request
    owner_id UUID NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_by UUID REFERENCES users(id),
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    channel VARCHAR(50) DEFAULT 'in_app', -- in_app, email, sms, whatsapp
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Consultations table
CREATE TABLE consultations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    staff_id UUID REFERENCES users(id),
    subject VARCHAR(200) NOT NULL,
    description TEXT,
    consultation_type VARCHAR(50), -- academic, financial, technical, general
    preferred_mode VARCHAR(50), -- remote, physical
    status VARCHAR(50) DEFAULT 'requested',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_number VARCHAR(50) UNIQUE NOT NULL,
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    staff_id UUID REFERENCES users(id),
    consultation_id UUID REFERENCES consultations(id),
    department_id UUID REFERENCES departments(id),
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    mode VARCHAR(50) DEFAULT 'physical', -- physical, remote
    location VARCHAR(200),
    status appointment_status DEFAULT 'scheduled',
    notes TEXT,
    cancellation_reason TEXT,
    rescheduled_from UUID REFERENCES appointments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Feedback table
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    service_request_id UUID REFERENCES service_requests(id),
    ticket_id UUID REFERENCES tickets(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    category VARCHAR(100),
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID,
    previous_value JSONB,
    new_value JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Staff working hours table
CREATE TABLE staff_working_hours (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    staff_id UUID REFERENCES users(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL, -- 0=Sunday, 1=Monday, ..., 6=Saturday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(staff_id, day_of_week)
);

-- System settings table
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSONB NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_students_student_number ON students(student_number);
CREATE INDEX idx_payments_transaction_reference ON payments(transaction_reference);
CREATE INDEX idx_payments_student_semester ON payments(student_id, semester_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_student ON tickets(student_id);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_queue_entries_queue ON queue_entries(queue_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);
CREATE INDEX idx_service_requests_student ON service_requests(student_id);
CREATE INDEX idx_appointments_student ON appointments(student_id);
CREATE INDEX idx_appointments_staff ON appointments(staff_id);
CREATE INDEX idx_appointments_date ON appointments(scheduled_date);

-- Insert default roles
INSERT INTO roles (name, description, permissions) VALUES
('student', 'Student role with basic access', '["view_profile", "view_finances", "submit_services", "view_tickets", "book_appointments"]'::jsonb),
('accounts_officer', 'Accounts Officer for financial operations', '["view_finances", "verify_payments", "reject_payments", "view_disputes", "process_financial_services", "generate_receipts"]'::jsonb),
('accounts_supervisor', 'Accounts Supervisor for escalated cases', '["view_finances", "approve_corrections", "review_waivers", "monitor_performance"]'::jsonb),
('registration_officer', 'Academic/Registration Officer', '["process_registration", "check_eligibility", "handle_registration_problems"]'::jsonb),
('faculty_staff', 'Faculty/Department Staff', '["handle_academic_requests", "handle_consultations", "process_departmental_approvals"]'::jsonb),
('ict_support', 'ICT Support Staff', '["handle_technical_support", "handle_account_access", "reset_passwords"]'::jsonb),
('queue_manager', 'Queue Manager', '["monitor_queues", "assign_tickets", "reassign_tickets", "manage_counters"]'::jsonb),
('admin', 'System Administrator', '["manage_users", "manage_roles", "manage_departments", "manage_programs", "manage_services", "configure_policies", "view_audit_logs"]'::jsonb),
('management', 'University Management', '["view_dashboards", "view_financial_reports", "view_service_reports", "view_metrics"]'::jsonb);

-- Insert default departments
INSERT INTO departments (name, code, description) VALUES
('Accounts and Finance', 'ACCT', 'Handles all financial matters'),
('Academic Registry', 'REG', 'Handles registration and academic records'),
('ICT', 'ICT', 'Information and Communication Technology'),
('Office of the Dean of Students', 'ODS', 'Student welfare and support'),
('College of Engineering and Technology', 'CET', 'Engineering programs'),
('College of Business and Economics', 'CBE', 'Business programs'),
('College of Education', 'COE', 'Education programs'),
('College of Humanities and Social Sciences', 'CHSS', 'Humanities programs');

-- Insert default service categories
INSERT INTO service_categories (name, code, description, department_id) VALUES
('Financial Services', 'FIN', 'All financial related services', (SELECT id FROM departments WHERE code = 'ACCT')),
('Registration Services', 'REG', 'Registration related services', (SELECT id FROM departments WHERE code = 'REG')),
('Academic Services', 'ACAD', 'Academic related services', (SELECT id FROM departments WHERE code = 'REG')),
('Technical Support', 'TECH', 'IT and technical support', (SELECT id FROM departments WHERE code = 'ICT')),
('General Services', 'GEN', 'General student services', (SELECT id FROM departments WHERE code = 'ODS'));

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('university_name', '"Uganda Christian University"', 'Official university name'),
('university_code', '"UCU"', 'University short code'),
('currency', '"UGX"', 'Default currency'),
('academic_year_start_month', '8', 'Month when academic year starts (August)'),
('support_email', '"support@ucu.ac.ug"', 'Support email address'),
('support_phone', '"+256-XXX-XXXXXX"', 'Support phone number');

COMMENT ON TABLE users IS 'System users including students, staff, and administrators';
COMMENT ON TABLE students IS 'Student profiles linked to users';
COMMENT ON TABLE staff IS 'Staff profiles linked to users';
COMMENT ON TABLE payments IS 'All payment transactions with verification status';
COMMENT ON TABLE semester_payment_policies IS 'Configurable payment policies per semester';
COMMENT ON TABLE tickets IS 'Service tickets for tracking student requests';
COMMENT ON TABLE audit_logs IS 'Audit trail for sensitive operations';
