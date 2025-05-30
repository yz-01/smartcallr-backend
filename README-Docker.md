# SmartCallr Backend - Docker Setup

Simple Docker setup for the Django backend.

## Quick Start

```bash
cd backend
docker compose up --build
```

## What's Included

- **Django Backend** - API running on port 8000
- **Uses Your Local Database** - Connects to your existing PostgreSQL

## Prerequisites

- Docker and Docker Compose v2
- Local PostgreSQL database running
- `.env` file with your API keys

## Environment Setup

Create `.env` file in backend directory:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=False

# Database (uses your local PostgreSQL)
DB_HOST=host.docker.internal
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password

# API Keys
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

## Commands

```bash
# Start services
docker compose up --build

# Stop services
docker compose down

# View logs
docker compose logs backend

# Rebuild and restart
docker compose down && docker compose up --build
```

## Access

- **API:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Health:** http://localhost:8000/leads/

## Notes

- Container connects to your local PostgreSQL database
- Recordings are saved to `./recordings` directory
- Environment variables loaded from `.env` file
- Hot reload not enabled (production setup)
