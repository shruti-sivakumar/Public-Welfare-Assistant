#  Public Welfare Assistant

A comprehensive AI-powered platform for managing public welfare schemes and citizen data with natural language query capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Azure](https://img.shields.io/badge/cloud-Azure-blue.svg)
![Docker](https://img.shields.io/badge/containerized-Docker-blue.svg)

##  Features

###  **AI-Powered Query Interface**
- **Natural Language to SQL**: Convert plain English queries to SQL using Azure OpenAI
- **Voice Input**: Speech-to-text integration with Azure Speech Service
- **Intelligent Fallback**: Pattern-based SQL generation when AI services are unavailable
- **Smart Chart Generation**: Automatic pie chart visualization for query results

###  **User Management & Security**
- **Role-Based Access Control (RBAC)**: Admin, Analyst, Officer, User roles
- **In-App Authentication**: Secure login system with session management
- **Access Logging**: Comprehensive activity tracking and audit trails
- **Permission Management**: Granular feature access control

###  **Data Management**
- **Azure SQL Database**: Scalable cloud database with 80+ districts coverage
- **Real-time Analytics**: Live dashboards with KPI metrics
- **Data Export**: CSV/Excel export capabilities with role-based permissions
- **Database Explorer**: Direct SQL query interface for advanced users

###  **Enterprise Features**
- **Containerized Deployment**: Docker-based architecture
- **Azure Integration**: Full Azure stack (SQL, OpenAI, Speech, Container Apps)
- **Responsive UI**: Professional Streamlit interface with custom styling
- **Multi-language Support**: Hindi and English language capabilities

##  Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend      │    │   Database      │
│   (Streamlit)   │◄──►│   (FastAPI)      │◄──►│  (Azure SQL)    │
│   - Web UI      │    │   - API Gateway  │    │  - Citizen Data │
│   - Auth        │    │   - AI Engine    │    │  - Schemes      │
│   - Charts      │    │   - SQL Gen      │    │  - Enrollments  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Azure Services │    │   AI Services    │    │   Monitoring    │
│  - Container    │    │  - OpenAI GPT    │    │  - Access Logs  │
│  - Speech       │    │  - Speech-to-Text│    │  - Analytics    │
│  - Storage      │    │  - NL Processing │    │  - Health Check │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

##  Quick Start

### Prerequisites
- Docker Desktop
- Azure Account with active subscription
- Git

### 1. Clone Repository
```bash
git clone https://github.com/shruti-sivakumar/Public-Welfare-Assistant.git
cd Public-Welfare-Assistant
```


### 2. Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individual containers
cd frontend
docker build -t welfare-frontend .

cd ../backend  
docker build -t welfare-backend .
```

### 3. Azure Deployment
```bash
# Login to Azure
az login

# Push to Azure Container Registry
az acr login --name your-registry
docker tag welfare-frontend your-registry.azurecr.io/frontend:latest
docker push your-registry.azurecr.io/frontend:latest

# Deploy to Azure Container Apps
az containerapp update --name welfare-frontend-app \
  --resource-group your-resource-group \
  --image your-registry.azurecr.io/frontend:latest
```

##  Usage

### For Citizens & Officers
1. **Login** with your assigned credentials
2. **Query Interface**: Ask questions in natural language
   - "How many citizens are enrolled in MGNREGA?"
   - "Show disbursements for PMAY in Maharashtra"
   - "List all schemes with their beneficiary counts"
3. **Voice Input**: Click microphone to speak your query
4. **View Results**: Data displayed in table format with chart visualization
5. **Export Data**: Download results as CSV/Excel (if permitted)

### For Administrators
1. **User Management**: Create, edit, and manage user accounts
2. **Access Control**: Configure role-based permissions
3. **Access Logs**: Monitor user activities and system usage
4. **System Monitoring**: View health metrics and performance data
5. **Data Management**: Direct database access and queries

##  Development

### Project Structure
```
Public-Welfare-Assistant/
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT license
├── README.md                # This file
├── frontend/                # Streamlit web application
│   ├── app.py               # Main application file
│   ├── access_logger.py     # Activity logging system
│   ├── in_app_auth.py       # Authentication module
│   ├── rbac.py              # Role-based access control
│   ├── azure_db.py          # Azure SQL Database integration
│   ├── azure_openai.py      # Azure OpenAI integration
│   ├── azure_speech.py      # Azure Speech Service integration
│   ├── database.py          # Database helper functions
│   ├── database_config.py   # Database configuration
│   ├── database_manager.py  # Database management utilities
│   ├── users.json           # User authentication data
│   ├── Dockerfile           # Frontend container definition
│   ├── requirements.txt     # Python dependencies

├── backend/                 # FastAPI backend service
│   ├── main.py              # FastAPI server
│   ├── auth.py              # Authentication APIs
│   ├── db.py                # Database connection utilities
│   ├── prompt_engine.py     # AI query processing engine
│   ├── Dockerfile           # Backend container definition
│   ├── requirements.txt     # Python dependencies
│   ├── routes/              # API route modules
│   │   ├── query.py         # Query processing endpoints
│   │   ├── summary.py       # Summary generation endpoints
│   │   └── verify.py        # Verification endpoints
├── database/                # Database scripts and schema
│   ├── schema.sql           # Database structure definition
│   ├── data.sql             # Sample/initial data
│   └── test_queries.sql     # Test SQL queries
├── docs/                    # Documentation files
│   └── schema_diagram.pdf   # Database schema diagram
```

### Local Development
```bash
# Frontend (Streamlit)
cd frontend
pip install -r requirements.txt
streamlit run app.py

# Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Testing
```bash
# Run comprehensive test queries
python -m pytest tests/

# Database connectivity test
python backend/db.py

# AI service test
python backend/azure_openai.py
```

##  Security Features

- **Encrypted Authentication**: Secure password hashing and session management
- **Role-Based Access**: Granular permissions for different user types
- **Audit Logging**: Complete activity tracking for compliance
- **Data Protection**: Encrypted data transmission and secure storage
- **Input Validation**: SQL injection prevention and input sanitization

##  Database Schema

### Core Tables
- **`citizens`**: Citizen demographic and contact information
- **`schemes`**: Government welfare scheme definitions
- **`enrollments`**: Citizen-scheme enrollment records
- **`disbursements`**: Payment and benefit distribution tracking
- **`officers`**: Administrative user accounts and roles

### Geographic Hierarchy
- **`states`**: Indian states and union territories
- **`districts`**: District-level administrative divisions
- **`villages`**: Village and locality information

##  API Documentation

### Authentication Endpoints
- `POST /auth/login` - User authentication
- `POST /auth/logout` - Session termination
- `GET /auth/profile` - User profile information

### Query Endpoints
- `POST /nl2sql` - Natural language to SQL conversion
- `POST /query/execute` - Direct SQL execution
- `GET /query/history` - Query history retrieval

### Data Endpoints
- `GET /citizens` - Citizen data with filtering
- `GET /schemes` - Available welfare schemes
- `GET /analytics` - Dashboard metrics and KPIs

##  Deployment Options

### Azure Cloud (Recommended)
- **Azure Container Apps**: Serverless container hosting
- **Azure SQL Database**: Managed database service
- **Azure OpenAI**: GPT-3-5-turbo integration for natural language processing
- **Azure Speech**: Voice-to-text conversion
- **Azure Container Registry**: Private container image storage

### Docker Compose
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=your_database_url
```

##  Monitoring & Analytics

### Access Logs
- User login/logout tracking
- Query execution logging
- Page access monitoring
- Data export tracking
- Administrative action logging

### System Metrics
- Database connection health
- API response times
- User activity statistics
- Error rate monitoring
- Resource utilization

##  Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add comprehensive docstrings for all functions
- Include unit tests for new features
- Update documentation for API changes
- Ensure backward compatibility

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- **Azure AI Services** for natural language processing capabilities
- **Streamlit Community** for the excellent web framework
- **FastAPI** for high-performance API development
- **Government of India** for welfare scheme data and requirements

##  Support

- **Documentation**: [Project Wiki](https://github.com/shruti-sivakumar/Public-Welfare-Assistant/wiki)
- **Issues**: [GitHub Issues](https://github.com/shruti-sivakumar/Public-Welfare-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shruti-sivakumar/Public-Welfare-Assistant/discussions)

##  Version History

### v2.0.0 (Current)
-  Azure OpenAI integration
-  Voice input with Azure Speech Service
-  Advanced access logging
-  Chart visualization with Plotly
-  Containerized deployment

### v1.0.0
-  Basic Streamlit interface
-  MySQL database integration
-  Role-based authentication
-  Simple query interface

---



