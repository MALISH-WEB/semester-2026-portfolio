# CampusQ - Entity Relationship Diagram (ERD)

## Database Schema Overview

This document describes the entity relationships in the CampusQ database for Uganda Christian University.

## Core Entities

### Users and Authentication

```
users (1) ──┬── (1) student
            ├── (1) staff
            └── (M) user_roles ── (1) roles
```

- **users**: Base user table for all system users
- **student**: Student-specific profile (one-to-one with users)
- **staff**: Staff-specific profile (one-to-one with users)
- **roles**: User roles (student, accounts_officer, admin, etc.)
- **user_roles**: Many-to-many relationship between users and roles

### Organizational Structure

```
departments (1) ── (M) programs
       │
       ├── (1) departments (self-reference for hierarchy)
       │
       └── (M) staff
```

- **departments**: University departments (Accounts, Registry, ICT, etc.)
- **programs**: Academic programs linked to departments

### Academic Structure

```
semesters (1) ── (M) student_semesters ── (M) students
     │
     └── (1) semester_payment_policies ── (M) payment_milestones
```

- **semesters**: Academic semesters
- **student_semesters**: Track which semesters each student has enrolled in
- **semester_payment_policies**: Configurable payment policies per semester
- **payment_milestones**: Payment milestone definitions (45%, 75%, 100%)

### Financial Domain

```
students (1) ── (M) payments
     │              │
     │              └── (1) payment_verifications (audit)
     │
     ├── (1) student_financial_accounts ── (1) semesters
     │
     └── (M) late_payment_charges ── (1) payment_milestones
     
payments (1) ── (1) receipts
```

- **student_financial_accounts**: Assessed tuition per student per semester
- **payments**: All payment transactions with status (pending/verified/rejected)
- **payment_verifications**: Audit trail for payment status changes
- **late_payment_charges**: Late payment penalties (unique per student/semester/milestone)
- **receipts**: Generated receipts for verified payments

### Service Request Domain

```
students (1) ── (M) service_requests ── (1) services
                        │
                        └── (1) tickets ── (M) ticket_status_history
                              │
                              ├── (1) queues ── (M) queue_entries
                              │
                              └── (M) ticket_assignments ── (1) users (staff)
```

- **service_categories**: Categories of services (Financial, Registration, etc.)
- **services**: Available services with routing rules
- **service_requests**: Student service requests
- **tickets**: Service tickets for tracking
- **ticket_status_history**: Audit trail for ticket status changes
- **ticket_assignments**: Track ticket assignment history
- **queues**: Virtual queues for physical services
- **queue_entries**: Queue positions for tickets
- **counters**: Service counters

### Appointments and Consultations

```
students (1) ── (M) consultations ── (1) staff (users)
                      │
                      └── (M) appointments ── (1) staff
```

- **consultations**: Consultation requests
- **appointments**: Scheduled appointments with status

### Documents and Notifications

```
documents: Polymorphic association (owner_type, owner_id)
notifications (M) ── (1) users
```

- **documents**: Uploaded documents with secure access
- **notifications**: In-app, email, SMS notifications

### Audit and System

```
audit_logs: System-wide audit trail
system_settings: Configurable system parameters
staff_working_hours: Staff availability for appointments
feedback: Student feedback on services
```

## Key Relationships

### One-to-One
- users ↔ student
- users ↔ staff
- student_financial_accounts: (student_id, semester_id) unique

### One-to-Many
- departments → programs
- departments → staff
- semesters → student_semesters
- students → payments
- students → service_requests
- tickets → ticket_status_history
- queues → queue_entries

### Many-to-Many
- users ↔ roles (via user_roles)
- students ↔ semesters (via student_semesters)

## Constraints

### Unique Constraints
- users.email
- students.student_number
- staff.staff_number
- payments.transaction_reference
- receipts.receipt_number
- tickets.ticket_number
- late_payment_charges: (student_id, semester_id, milestone_id)
- student_financial_accounts: (student_id, semester_id)

### Check Constraints
- payments.amount >= 0
- feedback.rating BETWEEN 1 AND 5

### Indexes
- users.email
- students.student_number
- payments.transaction_reference
- payments.status
- tickets.status
- tickets.assigned_to
- audit_logs.entity_type, entity_id
- audit_logs.created_at

## Data Flow Examples

### Payment Verification Flow
```
Payment (pending)
    ↓
Payment Verification (audit record)
    ↓
Payment (verified)
    ↓
Recalculate Financial Status
    ↓
Evaluate Milestones
    ↓
Generate Receipt
    ↓
Send Notification
```

### Service Request Flow
```
Student Request
    ↓
Service Identification
    ↓
Triage (Digital/Remote/Appointment/Queue)
    ↓
Ticket Creation
    ↓
Queue Assignment (if physical visit needed)
    ↓
Staff Assignment
    ↓
Resolution
    ↓
Feedback
```

## Security Considerations

1. **Soft Delete**: Critical tables have `deleted_at` for audit preservation
2. **Audit Trail**: payment_verifications, ticket_status_history, audit_logs
3. **Data Isolation**: Student data accessible only by authorized roles
4. **Document Security**: No public URLs; access controlled via API
