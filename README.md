# HR-AI Recruitment Platform

A production-ready, enterprise-grade AI-powered recruitment system that automates the entire hiring process from candidate sourcing to offer negotiation. Built for scale with FastAPI and agentic AI workflows.

## 🚀 Features

### Core Capabilities
- **Intelligent Job Analysis**: AI-powered job description parsing and skill extraction
- **Automated Candidate Sourcing**: BrightData LinkedIn integration for compliant candidate discovery
- **AI-Powered Matching**: Advanced candidate-job matching with confidence scoring
- **Multi-Channel Outreach**: Email and SMS communication with AI-generated personalized messages
- **Smart Interview Scheduling**: Calendar integration with Google Workspace and Microsoft 365
- **Real-time Dashboard**: Comprehensive analytics and pipeline management
- **Compliance Ready**: India-specific data protection and consent mechanisms

### Agentic AI Workflows
- **Job Requirements Analysis**: Automated skill extraction and keyword identification
- **Candidate Evaluation**: Multi-factor scoring and ranking algorithms
- **Personalized Outreach**: Context-aware message generation for different channels
- **Interview Feedback**: AI-assisted feedback drafting with human oversight
- **Negotiation Support**: Data-driven negotiation strategy recommendations

## 🛠 Tech Stack

- **Backend**: FastAPI with async/await support
- **Database**: PostgreSQL with async SQLAlchemy 2.0
- **Caching**: Redis for session management and task queuing
- **AI/ML**: OpenAI GPT-4 with LangChain for agentic workflows
- **Task Queue**: Celery with Redis broker
- **Data Sourcing**: BrightData LinkedIn scraper
- **Communication**: Twilio (SMS), SendGrid (Email)
- **Calendar**: Google Calendar & Microsoft 365 APIs
- **Authentication**: JWT with role-based access control
- **Deployment**: Docker & Docker Compose
- **Monitoring**: Structured logging with structlog

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (for containerized deployment)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HR_AI_INTERVIEWER
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start services with Docker**
   ```bash
   docker-compose up -d postgres redis
   ```

5. **Run the application**
   ```bash
   python start.py
   ```

### Docker Deployment

1. **Build and start all services**
   ```bash
   docker-compose up -d
   ```

2. **Check service health**
   ```bash
   docker-compose ps
   ```

3. **View logs**
   ```bash
   docker-compose logs -f backend
   ```

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/hr_ai_db

# AI Services
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# BrightData
BRIGHTDATA_USERNAME=your-brightdata-username
BRIGHTDATA_PASSWORD=your-brightdata-password

# Communication
TWILIO_ACCOUNT_SID=your-twilio-sid
SENDGRID_API_KEY=your-sendgrid-key

# Calendar Integration
GOOGLE_CLIENT_ID=your-google-client-id
MICROSOFT_CLIENT_ID=your-microsoft-client-id
```

### API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user

### Jobs Management
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/jobs/{id}` - Get job details
- `PUT /api/v1/jobs/{id}` - Update job

### Candidate Sourcing
- `POST /api/v1/sourcing/search` - Search candidates
- `GET /api/v1/candidates` - List candidates
- `POST /api/v1/candidates/bulk-approve` - Bulk approve candidates

### Interview Management
- `POST /api/v1/interviews/schedule` - Schedule interview
- `PUT /api/v1/interviews/{id}/approve` - Approve interview
- `PUT /api/v1/interviews/{id}/reschedule` - Reschedule interview

### Analytics
- `GET /api/v1/dashboard/overview` - Dashboard overview
- `GET /api/v1/dashboard/pipeline` - Pipeline analytics

## 🏗 Architecture

```
├── app.py                 # FastAPI application entry point
├── start.py              # Application startup script
├── celery_app.py         # Celery configuration
├── core/                 # Core application modules
│   ├── config.py         # Settings and configuration
│   ├── database.py       # Database setup and connection
│   ├── logging.py        # Structured logging configuration
│   └── security.py       # Authentication and security
├── models/               # SQLAlchemy database models
├── schemas/              # Pydantic request/response schemas
├── api/v1/endpoints/     # API route handlers
├── services/             # Business logic and external integrations
│   ├── ai_service.py     # OpenAI and LangChain integration
│   ├── brightdata_service.py  # LinkedIn scraping service
│   ├── outreach_service.py    # Multi-channel communication
│   └── calendar_service.py    # Calendar integration
└── routes/               # Legacy Flask routes (deprecated)
```

## 🔒 Security & Compliance

- **India Compliance**: Configured for Indian data protection laws (DPDP Act 2023)
- **Consent Management**: Opt-in email strategies with clear opt-out mechanisms
- **Data Security**: JWT authentication, password hashing, secure API endpoints
- **Rate Limiting**: Nginx-based rate limiting for API protection
- **CORS**: Configured for secure cross-origin requests

## 📈 Scaling Considerations

- **Async Architecture**: Built with FastAPI and async/await for high concurrency
- **Horizontal Scaling**: Stateless design supports multiple worker instances
- **Caching Strategy**: Redis caching for frequently accessed data
- **Task Queue**: Celery for background processing of AI tasks
- **Database Optimization**: Indexed queries and connection pooling

## 🧪 Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black .
flake8 .
mypy .
```

### Database Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue in the repository or contact the development team.
