# CampusQ Requirements Specification

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for CampusQ, a digital student-services platform for Uganda Christian University (UCU).

### 1.2 Scope
CampusQ is designed to reduce unnecessary physical visits and queues at UCU by enabling digital self-service, remote staff resolution, appointment scheduling, and virtual queuing only when genuinely necessary.

### 1.3 Definitions and Acronyms
- **UCU**: Uganda Christian University
- **RBAC**: Role-Based Access Control
- **API**: Application Programming Interface
- **ERD**: Entity Relationship Diagram

## 2. Overall Description

### 2.1 Product Perspective
CampusQ is a standalone web application that integrates with existing UCU systems through configurable adapters.

### 2.2 Product Functions
- Student authentication and profile management
- Financial services (balance inquiry, payment verification, disputes)
- Registration eligibility checking
- Service request submission and tracking
- Virtual queue management
- Appointment scheduling
- Notifications (in-app, email, SMS)
- Receipt generation
- Audit logging
- Reporting and dashboards

### 2.3 User Classes and Characteristics

#### Students
- Access personal financial and academic information
- Submit service requests
- Track request status
- Book appointments
- Join virtual queues when necessary

#### Accounts Officers
- Verify/reject payments
- Process financial services
- Generate receipts
- Resolve financial tickets

#### Accounts Supervisors
- Review escalated cases
- Approve waivers and corrections

#### Academic/Registration Officers
- Process registration requests
- Check eligibility
- Handle registration problems

#### ICT Support
- Handle technical issues
- Manage account access

#### Administrators
- Configure system settings
- Manage users and roles
- Define policies

#### Management
- View dashboards and reports
- Monitor KPIs

### 2.4 Operating Environment
- Backend: Python 3.11+, FastAPI, PostgreSQL 15+
- Frontend: React 18+, TypeScript
- Infrastructure: Docker, Docker Compose
- Deployment: Linux servers with HTTPS

### 2.5 Design and Implementation Constraints
- Must use specified technology stack
- Must comply with UCU branding guidelines
- Must support mobile-first responsive design
- Must implement proper security controls

### 2.6 Assumptions and Dependencies
- PostgreSQL database available
- Email/SMS gateway credentials provided for production
- UCU student data available for migration

## 3. System Features

### 3.1 Authentication and Authorization

#### 3.1.1 Login
- Users authenticate with email and password
- JWT tokens issued for session management
- Password reset functionality

#### 3.1.2 Role-Based Access Control
- Nine defined roles with specific permissions
- Backend enforcement of all authorization rules
- Students can only access their own data

### 3.2 Financial Services

#### 3.2.1 Balance Inquiry
- View assessed tuition
- View verified payments
- View pending payments
- Calculate outstanding balance
- Display payment percentage

#### 3.2.2 Payment Verification
- Accounts officers verify submitted payments
- Verified payments affect eligibility
- Pending/rejected payments do not affect eligibility
- Audit trail maintained

#### 3.2.3 Payment Milestones
- Configurable percentages (default 45%, 75%, 100%)
- Configurable deadlines
- Automatic milestone evaluation
- Late charge assessment (configurable, default UGX 50,000)

#### 3.2.4 Registration Eligibility
- Check 45% payment threshold
- Check registration dates
- Check academic requirements
- Display clear reasons for ineligibility
- Show additional amount required

### 3.3 Service Request Management

#### 3.3.1 Service Catalogue
- Database-driven service definitions
- Extensible without code changes
- Services linked to departments

#### 3.3.2 Triage Engine
- Automatic routing based on service type
- Determine if digital completion possible
- Route to remote staff if needed
- Create appointment if scheduled attendance needed
- Add to virtual queue only if physical visit necessary

#### 3.3.3 Ticketing
- Unique ticket numbers
- Status tracking (WAITING, CALLED, SERVING, etc.)
- Assignment to staff
- Escalation support
- Resolution notes

### 3.4 Virtual Queue Management

#### 3.4.1 Queue Creation
- Only when physical visit necessary
- Department/service-based queues
- Capacity limits

#### 3.4.2 Queue Operations
- Position calculation
- Estimated wait time
- Call next ticket
- Mark as serving
- Complete or cancel

### 3.5 Appointments

#### 3.5.1 Scheduling
- Staff working hours configuration
- Time slot availability
- Booking by students
- Confirmation notifications

#### 3.5.2 Management
- Cancellation
- Rescheduling
- Reminder notifications

### 3.6 Notifications

#### 3.6.1 Channels
- In-app notifications
- Email (configurable SMTP)
- SMS (configurable provider)
- WhatsApp (future integration point)

#### 3.6.2 Events
- Payment submitted/verified/rejected
- Milestone achieved/missed
- Late charge applied
- Registration eligible/blocked
- Ticket created/updated/resolved
- Appointment reminders

### 3.7 Receipts

#### 3.7.1 Generation
- Automatic on payment verification
- Unique receipt numbers
- PDF format

#### 3.7.2 Access
- Student download
- Staff reissue capability

### 3.8 Audit Logging

#### 3.8.1 Audited Operations
- Payment verification/rejection
- Financial corrections
- Late charge creation/waiver
- Registration decisions
- Ticket reassignments
- Policy changes
- Role changes

#### 3.8.2 Audit Data
- User ID
- Action performed
- Entity type and ID
- Previous and new values
- Timestamp
- IP address

### 3.9 Reporting

#### 3.9.1 Financial Reports
- Total tuition assessed
- Verified payments
- Outstanding balances
- Students by payment percentage ranges
- Pending verifications
- Charges assessed/waived

#### 3.9.2 Service Reports
- Requests received/resolved/pending
- Response times
- Resolution times
- Escalations
- Satisfaction ratings

#### 3.9.3 Queue-Busting Metrics
- Physical visits avoided
- Digital completion percentage
- Remote resolution percentage
- Virtual vs physical waiting times
- First-contact resolution rate

## 4. External Interface Requirements

### 4.1 User Interfaces
- Mobile-first responsive web interface
- Professional UCU-branded appearance
- Clear status indicators
- Understandable error messages

### 4.2 Hardware Interfaces
- None specified (web application)

### 4.3 Software Interfaces
- PostgreSQL database
- SMTP email server
- SMS gateway API (optional)
- Future: Student Information System integration
- Future: Payment gateway integration

### 4.4 Communications Interfaces
- HTTPS for production
- RESTful API
- OpenAPI documentation

## 5. Non-Functional Requirements

### 5.1 Performance
- Page load < 3 seconds on 3G networks
- API response < 500ms for standard queries
- Support 1000+ concurrent users

### 5.2 Security
- Secure password hashing (bcrypt)
- JWT token authentication
- Backend authorization enforcement
- SQL injection protection
- XSS protection
- Rate limiting
- Secure file uploads
- Data isolation between students

### 5.3 Reliability
- 99.5% uptime target
- Database backups daily
- Transaction integrity for financial operations

### 5.4 Maintainability
- Clean code architecture
- Separation of concerns
- Comprehensive documentation
- Automated testing

### 5.5 Scalability
- Horizontal scaling capability
- Database connection pooling
- Efficient queries with indexes

### 5.6 Accessibility
- WCAG 2.1 Level AA compliance target
- Keyboard navigation
- Screen reader compatibility

## 6. Acceptance Criteria

The system is complete when:

1. ✅ Secure student registration/login works
2. ✅ Students can view financial status
3. ✅ Verified payment percentage calculated correctly
4. ✅ 45% eligibility check works
5. ✅ 75% milestone evaluation works
6. ✅ 100% milestone evaluation works
7. ✅ Deadlines are configurable
8. ✅ Late charges configurable and correctly evaluated
9. ✅ Duplicate charges prevented
10. ✅ Pending payments do not affect eligibility
11. ✅ Students can submit services digitally
12. ✅ Requests routed correctly
13. ✅ Virtual tickets work
14. ✅ Virtual queues work
15. ✅ Appointments work
16. ✅ Staff can process requests
17. ✅ Notifications work
18. ✅ Receipts work
19. ✅ Audit logs work
20. ✅ RBAC works
21. ✅ Student data isolation works
22. ✅ Reports work
23. ✅ Physical visits avoided measurable
24. ✅ Mobile and desktop interfaces work
25. ✅ Automated tests pass
26. ✅ Deployment succeeds
27. ✅ Documentation complete

## 7. Appendices

### 7.1 Financial Examples

**Example 1: 45% Achievement**
```
Tuition: UGX 2,000,000
Verified: UGX 900,000
Payment %: 45%
Registration: ELIGIBLE
```

**Example 2: Below Threshold**
```
Tuition: UGX 2,000,000
Verified: UGX 840,000
Payment %: 42%
Registration: BLOCKED
Additional required: UGX 60,000
```

**Example 3: Full Payment**
```
Tuition: UGX 2,000,000
Verified: UGX 2,000,000
Payment %: 100%
Financial Clearance: COMPLETE
```

### 7.2 Ticket State Machine

Valid states:
- WAITING
- CALLED
- SERVING
- IN_PROGRESS
- PENDING_STUDENT
- PENDING_STAFF
- ESCALATED
- RESOLVED
- COMPLETED
- CANCELLED
- REJECTED

### 7.3 Service Outcomes

Each service request tracked with outcome:
- DIGITAL: Completed online without staff intervention
- REMOTE: Resolved by staff remotely
- APPOINTMENT: Required scheduled appointment
- VIRTUAL_QUEUE: Joined virtual queue
- PHYSICAL: Required physical visit
