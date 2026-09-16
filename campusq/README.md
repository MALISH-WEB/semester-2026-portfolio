# CampusQ - Uganda Christian University Digital Student Services Platform

## Overview

CampusQ is a comprehensive digital student services platform designed for Uganda Christian University (UCU). The platform enables students to complete services digitally, obtain automated decisions, communicate remotely with staff, schedule appointments, or join virtual queues only when genuinely necessary.

## Primary Objective

**Reduce unnecessary physical visits and queues at UCU** by allowing students to:
- Complete services digitally through automated self-service
- Obtain automated eligibility decisions
- Communicate remotely with staff
- Schedule appointments when needed
- Join virtual queues only when physical presence is truly required

## Technology Stack

### Backend
- **Python 3.12+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **PostgreSQL** - Primary database
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **Modern responsive CSS** - Mobile-first design

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Alembic** - Database migrations

## Core Features

### Financial Services
- Balance Inquiry
- Payment Verification
- Balance Dispute Resolution
- Retake Payment Processing
- Recess Semester Payment
- Graduation Payment
- Sponsored Student Financial Services
- Receipt Generation
- Financial Consultation

### Registration Services
- 45% Registration Eligibility Check
- Semester Registration
- Registration Problem Resolution
- Academic Consultation

### Service Triage System
The platform implements an intelligent triage system that routes requests based on:
1. **Digital Self-Service** - Automatically completed by the system
2. **Remote Staff Resolution** - Handled by staff without physical visit
3. **Appointment** - Scheduled meeting with staff
4. **Virtual Queue** - Only when physical presence is necessary

### Financial Policy Engine
Configurable semester payment policies with:
- Initial milestone (default 45%)
- Second milestone (default 75%)
- Final milestone (100%)
- Configurable late payment charges
- Flexible charge frequencies

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL 14+ (or use Docker)

### Using Docker Compose

```bash
# Clone the repository
cd campusq

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env

# Run database migrations
# (Use the init.sql script in database/)

# Start the server
python -m uvicorn app.main:app --reload
```

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## User Roles

| Role | Description |
|------|-------------|
| Student | Submit requests, view financial status, track tickets |
| Accounts Officer | Verify payments, process financial requests |
| Accounts Supervisor | Review escalated cases, approve waivers |
| Academic Officer | Process registration, handle academic services |
| Faculty Staff | Handle departmental requests, consultations |
| ICT Support | Technical support, account issues |
| Queue Manager | Monitor queues, assign tickets |
| Administrator | System configuration, user management |
| Management | Dashboards, reports, analytics |

## Project Structure

```
campusq/
├── backend/
│   └── app/
│       ├── api/          # API endpoints
│       ├── core/         # Configuration, security, JWT
│       ├── db/           # Database connection
│       ├── models/       # SQLAlchemy models
│       ├── schemas/      # Pydantic schemas
│       ├── services/     # Business logic
│       └── main.py       # Application entry
├── database/
│   └── init.sql          # Database schema
├── frontend/             # React application
├── docker/               # Docker configurations
├── docs/                 # Documentation
├── tests/                # Test suite
├── scripts/              # Utility scripts
├── docker-compose.yml
├── .env.example
└── README.md
```

## Key Business Rules

### Payment Calculation
```
Payment Percentage = (Total Verified Payments / Assessed Tuition) × 100
```

Only **VERIFIED** payments affect eligibility. PENDING, REJECTED, and CANCELLED payments do not count.

### Registration Eligibility
Students must meet the minimum payment threshold (default 45%) to be eligible for registration.

### Late Payment Charges
Automatically assessed when milestones are missed after deadlines. Configurable frequency:
- ONCE_PER_MILESTONE
- ONCE_PER_SEMESTER
- RECURRING

## Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Backend authorization enforcement
- SQL injection protection
- XSS prevention
- Input validation
- Audit logging for sensitive operations
- Secure password hashing with bcrypt

## Testing

```bash
# Run tests
cd backend
pytest

# Run with coverage
pytest --cov=app
```

## Environment Variables

See `.env.example` for all configurable options:
- Database credentials
- JWT secrets
- Email/SMS configuration
- File upload limits
- Rate limiting settings

## Documentation

- [Requirements Specification](docs/REQUIREMENTS.md)
- [Entity Relationship Diagram](docs/ERD.md)

## License

Proprietary - Uganda Christian University

## Contact

For support, contact the UCU ICT Department.
