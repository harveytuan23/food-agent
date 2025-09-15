# 🛠️ Technical Architecture Documentation

## Project Overview
The Smart Food Management Assistant is an AI-powered ingredient inventory management system that integrates multiple modern technologies to provide an intelligent food management experience.

## 🏗️ Overall Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LINE Bot      │    │   FastAPI       │    │   Google Sheets │
│   (User Interface)│◄──►│   (API Service) │◄──►│   (Data Storage)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   LangChain     │
                       │   (AI Agent)    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI        │
                       │   (GPT-4o-mini) │
                       └─────────────────┘
```

## 🔧 Core Technology Stack

### 1. Backend Framework
- **FastAPI** - Modern Python Web Framework
  - High-performance asynchronous processing
  - Automatic API documentation generation
  - Type hint support
  - Built-in data validation

### 2. AI & Machine Learning
- **LangChain** - AI Application Development Framework
  - Agent system management
  - Tool chain integration
  - Prompt template management
  - Output parsers

- **OpenAI GPT-4o-mini** - Large Language Model
  - Natural language understanding
  - Intelligent decision making
  - Tool calling capabilities
  - Context memory

### 3. Data Storage
- **Google Sheets API** - Cloud Spreadsheet Service
  - Real-time data synchronization
  - Automatic backup
  - Collaboration features
  - Version control

### 4. Communication & Notifications
- **LINE Messaging API** - Instant Messaging Platform
  - User interaction interface
  - Push notifications
  - Rich media support
  - Group management

- **n8n** - Workflow Automation
  - Scheduled task execution
  - API integration
  - Conditional logic processing
  - Multi-platform notifications

## 📚 Development Tools & Libraries

### Python Core Libraries
```python
# Web Framework
fastapi==0.104.1
uvicorn==0.24.0

# AI & Machine Learning
langchain==0.1.0
langchain-openai==0.0.2
langchain-core==0.1.0
openai==1.3.0

# Data Processing
pydantic==2.5.0
python-dotenv==1.0.0

# Google Services
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
gspread==5.12.0

# LINE Bot
line-bot-sdk==3.5.0

# HTTP Requests
httpx==0.25.0
requests==2.31.0

# Logging & Monitoring
logging
datetime
```

### Development Environment Tools
- **Python 3.11+** - Programming Language
- **pip** - Package Management
- **venv** - Virtual Environment
- **Git** - Version Control

## 🔄 System Flow

### 1. User Interaction Flow
```
User sends message → LINE Bot → FastAPI → LangChain Agent → Tool calls → Google Sheets → Response to user
```

### 2. Automated Notification Flow
```
Scheduled trigger → n8n → API call → Check expiring ingredients → Send notification → LINE user
```

### 3. Data Processing Flow
```
User input → Text parsing → Structured data → Google Sheets storage → Real-time sync
```

## 🏛️ Architecture Patterns

### 1. Agent Pattern
- **Intelligent Agent**: LangChain Agent as core decision engine
- **Tool Calling**: Dynamic selection and execution of appropriate tools
- **State Management**: Maintain conversation context and memory

### 2. Microservices Architecture
- **API Service**: FastAPI provides RESTful API
- **Data Service**: Google Sheets as data layer
- **Notification Service**: LINE and n8n handle notifications

### 3. Event-Driven Architecture
- **Webhook**: LINE Bot event handling
- **Scheduled Tasks**: n8n workflow scheduling
- **Asynchronous Processing**: FastAPI async request processing

## 🔐 Security & Authentication

### 1. API Security
- **Environment Variables**: Encrypted storage of sensitive information
- **Signature Verification**: LINE Webhook signature verification
- **Error Handling**: Complete exception handling mechanism

### 2. Data Security
- **Google OAuth**: Service account authentication
- **Access Control**: Principle of least privilege
- **Data Encryption**: Transport and storage encryption

### 3. Access Control
- **API Limits**: Request rate limiting
- **User Authentication**: LINE user identity verification
- **Logging**: Complete operation logs

## 📊 Data Models

### 1. Ingredient Data Structure
```python
class IngredientInfo(BaseModel):
    name: str                    # Ingredient name
    quantity: float | None       # Quantity
    unit: str | None            # Unit
    expires_at: str | None      # Expiration date
    location: str | None        # Storage location
    notes: str | None           # Notes
```

### 2. Google Sheets Structure
```
| ID | Name | Quantity | Unit | Expiration Date | Storage Location | Notes | Created Time | Updated Time |
```

### 3. API Response Format
```json
{
  "success": true,
  "has_expiring": true,
  "message": "Expiration reminder content",
  "timestamp": "2025-09-14T12:00:00Z"
}
```

## 🚀 Deployment & Operations

### 1. Local Development
```bash
# Environment Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start Service
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Production Environment
- **Containerization**: Docker support
- **Load Balancing**: Multi-instance deployment
- **Monitoring**: Log and metrics collection
- **Backup**: Automatic data backup

### 3. CI/CD
- **Version Control**: Git workflow
- **Automated Testing**: Unit tests and integration tests
- **Deployment**: Automated deployment process

## 🔧 Tools & Services

### 1. Development Tools
- **IDE**: VS Code, PyCharm
- **API Testing**: Postman, curl
- **Database Management**: Google Sheets Web UI
- **Log Analysis**: Built-in logging system

### 2. Third-party Services
- **OpenAI API**: AI model service
- **Google Cloud**: Spreadsheet and authentication services
- **LINE Platform**: Communication and notification services
- **n8n**: Workflow automation

### 3. Monitoring & Analytics
- **Application Logs**: Structured log recording
- **Error Tracking**: Exception handling and reporting
- **Performance Monitoring**: Response time and throughput
- **Usage Statistics**: User behavior analysis

## 📈 Scalability Design

### 1. Horizontal Scaling
- **Stateless Design**: No dependencies between services
- **Load Balancing**: Multi-instance deployment
- **Data Sharding**: Google Sheets partitioning

### 2. Feature Extension
- **Plugin Architecture**: Modular tool design
- **API Version Control**: Backward compatibility
- **Configuration Management**: Environment variable configuration

### 3. Performance Optimization
- **Caching Mechanism**: Local data caching
- **Asynchronous Processing**: Non-blocking operations
- **Connection Pooling**: Database connection optimization

## 🔮 Future Technology Roadmap

### 1. Short-term Goals
- **Data Analytics**: Ingredient usage pattern analysis
- **Prediction Features**: Expiration time prediction
- **Multi-language Support**: Internationalization support

### 2. Medium-term Goals
- **Machine Learning**: Intelligent recommendation system
- **Image Recognition**: Ingredient image recognition
- **Voice Interaction**: Voice command support

### 3. Long-term Goals
- **IoT Integration**: Smart refrigerator connection
- **Blockchain**: Food safety traceability
- **AR/VR**: Virtual kitchen experience

## 📝 Technical Decision Records

### 1. Why FastAPI?
- High-performance asynchronous processing
- Automatic API documentation generation
- Modern Python feature support
- Active community and ecosystem

### 2. Why LangChain?
- Mature AI Agent framework
- Rich tool ecosystem
- Excellent OpenAI integration
- Flexible prompt management

### 3. Why Google Sheets?
- No additional database setup required
- Real-time collaboration features
- Automatic backup and version control
- Easy to view and edit

### 4. Why LINE?
- High penetration rate in Taiwan
- Rich API functionality
- Excellent user experience
- Stable service quality

---

## 📞 Technical Support

For technical issues, please refer to:
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [LangChain Official Documentation](https://python.langchain.com/)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [LINE Messaging API Documentation](https://developers.line.biz/en/docs/messaging-api/)
- [n8n Official Documentation](https://docs.n8n.io/)
