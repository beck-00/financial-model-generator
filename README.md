# Financial Model Generator

A comprehensive, microservices-based web application that enables financial analysts to create dynamic Excel financial models from uploaded management accounts. The application provides a guided workflow to upload historical financial data, map it to standardized line items (with AI-driven auto-categorization), configure assumptions and scenarios, and export professional, fully functional Excel models with formulas and scenario management capabilities.

## 🎯 Scope & Purpose

This application transforms raw management accounts into professional, three-statement financial models featuring:

- **Three-Statement Integration**: Fully integrated Profit & Loss, Balance Sheet, and Cash Flow statements.
- **Dynamic Scenario Analysis**: Support for Base, Optimistic, and Pessimistic scenarios with dropdown selection.
- **DCF Valuation**: Complete discounted cash flow analysis with terminal value calculations.
- **Industry-Specific Templates**: Pre-configured line items for SaaS, retail, manufacturing, and consulting businesses.
- **AI-Driven Categorization**: Automatic mapping of management accounts to standard line items and generation of line items from business descriptions using NLP.
- **Professional Excel Output**: Formatted Excel files with formulas, data validation, and hyperlinked navigation.

## 🏗️ Application Structure

```
financial-model-generator/
├── docker-compose.yml                 # Orchestrates microservices (web, auth, model-generator, ai)
├── .env.example                       # Template for environment variables
├── README.md                          # Project documentation
├── services/                          # Microservices
│   ├── auth/                          # Authentication service
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                # FastAPI entry point
│   │   │   ├── routes.py              # Login, register, token refresh endpoints
│   │   │   ├── models.py              # Pydantic models (User, Token)
│   │   │   ├── utils.py               # JWT, password hashing
│   │   │   └── db.py                  # SQLAlchemy for database
│   │   ├── tests/                     # Unit/integration tests
│   │   │   └── test_auth.py
│   │   ├── Dockerfile                 # Builds auth service
│   │   ├── requirements.txt           # fastapi, uvicorn, sqlalchemy, passlib, pyjwt
│   │   └── pyproject.toml
│   ├── model-generator/               # Financial modeling and Excel generation
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                # FastAPI entry point
│   │   │   ├── routes.py              # Model generation, mapping, scenarios
│   │   │   ├── financial_model.py     # Core modeling logic
│   │   │   ├── line_item_generator.py # Line item generation, calls AI service
│   │   │   ├── excel_handler.py       # Excel parsing/generation
│   │   │   ├── models.py              # Pydantic models (Assumptions, Scenarios)
│   │   │   └── utils.py               # File handling, API clients
│   │   ├── tests/
│   │   │   └── test_model.py
│   │   ├── Dockerfile                 # Builds model-generator service
│   │   ├── requirements.txt           # fastapi, pandas, openpyxl
│   │   └── pyproject.toml
│   ├── ai/                            # AI-driven auto-categorization
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                # FastAPI entry point
│   │   │   ├── routes.py              # Categorization, business analysis endpoints
│   │   │   ├── ai_categorizer.py      # NLP-based categorization logic
│   │   │   ├── models.py              # Pydantic models (LineItem, BusinessDescription)
│   │   │   ├── utils.py               # Text preprocessing, model loading
│   │   │   └── db.py                  # Optional: Store mapping rules
│   │   ├── tests/
│   │   │   └── test_ai.py
│   │   ├── Dockerfile                 # Builds AI service
│   │   ├── requirements.txt           # fastapi, transformers, sentence-transformers
│   │   └── pyproject.toml
│   └── web/                           # Web frontend
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py                # Flask entry point
│       │   ├── routes.py              # Web routes, calls other services
│       │   ├── utils.py               # API clients, session management
│       │   └── config.py              # Service URLs from env vars
│       ├── static/                    # CSS, JS, sample data
│       │   ├── css/
│       │   │   └── custom.css         # Custom styling, dark theme
│       │   ├── js/
│       │   │   └── main.js            # Frontend JavaScript
│       │   └── sample_data.xlsx       # Sample data for testing
│       ├── templates/                 # Jinja2 templates
│       │   ├── base.html             # Base template with Bootstrap
│       │   ├── index.html            # Landing page
│       │   ├── upload.html           # File upload interface
│       │   ├── business_description.html # Business type selection
│       │   ├── line_items.html       # Line items review
│       │   ├── mapping.html          # Account mapping interface
│       │   ├── periods.html          # Period configuration
│       │   ├── assumptions.html      # Assumptions configuration
│       │   ├── scenarios.html        # Scenario management
│       │   └── export.html           # Model export and download
│       ├── tests/
│       │   └── test_web.py
│       ├── Dockerfile                 # Builds web service
│       ├── requirements.txt           # flask, requests
│       └── pyproject.toml
├── shared/                            # Shared utilities
│   ├── db/                            # Shared SQLAlchemy models/migrations
│   └── utils/                         # Common logging, error handling
├── attached_assets/                   # Generated Excel files (Docker volume)
└── sample_files/                      # Example Excel files
    ├── SaaS_Company_Monthly_Data.xlsx
    ├── Retail_Company_Monthly_Data.xlsx
    └── Manufacturing_Company_Monthly_Data.xlsx
```

## 🔧 Core Components

### 1. **Web Service (`services/web/`)**
- Flask-based frontend with Jinja2 templates.
- Handles user workflow, rendering UI, and calling `auth`, `model-generator`, and `ai` services via HTTP.
- Uses Bootstrap 5 for responsive UI and Feather Icons for consistent iconography.

### 2. **Auth Service (`services/auth/`)**
- FastAPI-based service for user authentication.
- Implements JWT-based auth with endpoints for login, registration, and token refresh.
- Optional PostgreSQL integration for user storage.

### 3. **Model-Generator Service (`services/model-generator/`)**
- FastAPI-based service for financial model creation and Excel generation.
- Handles three-statement modeling, DCF valuation, and scenario analysis.
- Calls `ai` service for line item categorization and generation.

### 4. **AI Service (`services/ai/`)**
- FastAPI-based service for AI-driven auto-categorization.
- Uses NLP (e.g., `sentence-transformers`) to map management accounts to standard line items and generate line items from business descriptions.
- Endpoints: `/categorize` for line item mapping, `/analyze-business` for business-specific line items.

## 🚀 Key Features

### Financial Modeling
- **Historical Data Integration**: Upload and process Excel-based management accounts.
- **Automated Mapping**: AI-driven mapping of management accounts to standardized line items.
- **Formula Generation**: Excel formulas for revenue growth, expense ratios, and working capital.
- **Three-Statement Linkage**: Integrated Profit & Loss, Balance Sheet, and Cash Flow statements.

### AI-Driven Categorization
- **Line Item Mapping**: Automatically categorizes raw management account entries (e.g., “Software Subscriptions” → “Cost of Revenue - Subscriptions”) using NLP.
- **Business Description Analysis**: Generates industry-specific line items (e.g., ARR, churn) based on business descriptions.

### Scenario Analysis
- **Multiple Scenarios**: Base, Optimistic, and Pessimistic cases with configurable assumptions.
- **Dynamic Selection**: Excel dropdown for real-time scenario switching.
- **Assumption Categories**: Organized by growth rates, margins, and working capital metrics.

### DCF Valuation
- **Free Cash Flow Calculations**: Firm and Equity FCF methods.
- **Terminal Value**: Configurable growth rates and exit multiples.
- **Net Debt Breakdown**: Linked to balance sheet items.
- **Enterprise Value**: Complete valuation with present value calculations.

### Excel Output Features
- **Professional Formatting**: Blue headers, formula highlighting.
- **Data Validation**: Dropdown lists for scenario selection.
- **Hyperlinked Navigation**: Table of contents with clickable sheet links.
- **Hidden Historical Columns**: Clean forecast-focused presentation.
- **Formula Transparency**: All calculations visible and auditable.

## 🛠️ Technical Architecture

### Backend Stack
- **Frameworks**: Flask (web), FastAPI (auth, model-generator, ai).
- **Data Processing**: Pandas for data manipulation, openpyxl for Excel generation.
- **AI Processing**: `sentence-transformers` for NLP, optional fine-tuned BERT models.
- **Session Management**: Flask sessions for web, JWT for API authentication.
- **Security**: Werkzeug for secure file handling, JWT for API access.

### Frontend Stack
- **UI Framework**: Bootstrap 5 with custom dark theme.
- **JavaScript**: jQuery for DOM manipulation and AJAX.
- **Icons**: Feather Icons library.
- **Styling**: CSS custom properties and Bootstrap utilities.

### Data Flow
1. **Upload Phase**: Web service handles Excel file uploads, validates, and sends to model-generator.
2. **Business Analysis**: Web collects business description, sends to AI service for line item generation.
3. **Mapping Phase**: Model-generator uses AI service to map management accounts to standard line items.
4. **Configuration**: Web collects period and assumption inputs, sends to model-generator.
5. **Generation**: Model-generator creates Excel model with formulas and formatting.
6. **Export**: Web serves downloadable Excel file from shared storage.

## 📋 Usage Workflow
1. **Authenticate**: Log in via auth service to access the app.
2. **Upload Management Accounts**: Upload Excel files with historical financial data.
3. **Describe Business**: Select or input business description for industry-specific line items.
4. **Review AI-Generated Line Items**: Confirm AI-suggested line items from business description.
5. **Map Accounts**: Review AI-mapped management accounts to standardized line items.
6. **Configure Periods**: Set forecast timeline and periodicity.
7. **Set Assumptions**: Define growth rates, margins, and operational metrics.
8. **Create Scenarios**: Configure Base, Optimistic, and Pessimistic cases.
9. **Export Model**: Download professional Excel financial model.

## 🔒 Security Features
- File type validation (Excel only, 16MB limit).
- Secure filename handling with Werkzeug.
- JWT-based authentication for API endpoints.
- Session-based temporary storage in web service.
- Automatic cleanup of temporary files.

## 📊 Supported Industries
- **SaaS/Technology**: Subscription revenue, churn rates, customer acquisition costs.
- **Retail**: Inventory turnover, seasonal adjustments, cost of goods sold.
- **Manufacturing**: Production capacity, raw materials, depreciation.
- **Consulting**: Billable hours, utilization rates, project-based revenue.

## 🎨 Design Principles
- **User-Friendly**: Step-by-step wizard interface for non-technical users.
- **Professional Output**: Investment-grade Excel models with proper formatting.
- **Transparency**: All formulas and calculations visible and auditable.
- **Flexibility**: Configurable assumptions and multiple scenario support.
- **Industry-Specific**: AI-driven templates tailored to business models.

## 🚀 Local Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11 or higher (for local dependency installation)
- Optional: Node.js/npm (if managing frontend dependencies locally)

### Installation & Running
1. **Clone or download the repository**
   ```bash
   cd financial-model-generator
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to configure service URLs, database credentials, etc.

3. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Web UI: `http://localhost:5000`
   - Auth API: `http://localhost:8001`
   - Model-Generator API: `http://localhost:8002`
   - AI API: `http://localhost:8003`

### Alternative Installation (Without Docker)
1. Create virtual environments for each service:
   ```bash
   cd services/web && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd services/auth && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd services/model-generator && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd services/ai && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   ```
2. Run each service separately:
   ```bash
   cd services/web && gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
   cd services/auth && uvicorn app.main:app --host 0.0.0.0 --port 8001
   cd services/model-generator && uvicorn app.main:app --host 0.0.0.0 --port 8002
   cd services/ai && uvicorn app.main:app --host 0.0.0.0 --port 8003
   ```

### Stopping the Application
- Docker: `docker-compose down`
- Manual: Press `Ctrl+C` in each terminal or use `kill` on the process IDs.

## 🛠️ Testing
Each service includes a `tests/` directory with unit and integration tests:
- Run tests for a service:
  ```bash
  cd services/<service> && pytest tests/
  ```

## 📦 Deployment
- **Cloud**: Deploy using AWS ECS, Google Cloud Run, or Render with Docker images.
- **VPS**: Use Docker Compose or Kubernetes for orchestration.
- **Reverse Proxy**: Set up Nginx or Traefik to route traffic to the web service.