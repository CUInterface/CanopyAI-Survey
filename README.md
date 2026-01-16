# CanopyAI Survey

A Flask-based survey application for Credit Union stakeholders to rank and prioritize questions for the CanopyAI system.

## Overview

This app allows CU stakeholders to vote on pre-generated questions across three categories:
- **Marketing** - Member demographics, engagement, cross-sell opportunities
- **Loans** - Pipeline management, production tracking, risk assessment
- **Live Transactions** - Real-time monitoring, daily operations, alerts

Users can also suggest their own questions for the community to vote on.

## Features

- Email-based authentication (prevents duplicate votes)
- Upvote/downvote system with real-time updates
- User-submitted question suggestions
- Results dashboard with category filtering
- CSV export for analytics

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: Jinja2 templates, Bootstrap 5
- **Deployment**: Azure App Service ready

## Local Development

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Seed the database with questions
python seed_questions.py

# Run the app
python app.py
```

Visit http://localhost:5000

## Deployment (Azure Container Apps)

This app deploys via GitHub Actions to Azure Container Apps.

### Prerequisites

1. Azure Container Registry (ACR)
2. Azure Container Apps environment
3. GitHub repository secrets:

| Secret | Description |
|--------|-------------|
| `ACR_NAME` | Azure Container Registry name |
| `ACR_USERNAME` | ACR admin username |
| `ACR_PASSWORD` | ACR admin password |
| `AZURE_RESOURCE_GROUP` | Resource group name |
| `AZURE_CREDENTIALS` | Azure service principal JSON |

### Deploy

Push to `master` branch triggers automatic build and deploy.

### Manual Docker Build

```bash
docker build -t canopyai-survey .
docker run -p 8000:8000 canopyai-survey
```

## Related

- [Vyrdia Financial AI Issue #84](https://github.com/CUInterface/Vyrdia_Financial_AI/issues/84) - Original question set
