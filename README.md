# SmartCallr - AI-Powered Call Management System

A full-stack web application for managing leads and calls with AI transcription and summarization.

## Features

- **Lead Management** - Create, edit, and organize leads with international phone support
- **Call Management** - Make calls via Twilio integration
- **AI Transcription** - Automatic call transcription using OpenAI Whisper
- **AI Summarization** - Smart call summaries with key insights
- **Real-time Updates** - Live call status and progress tracking
- **Notes & Recording** - Save notes during calls and download recordings

## Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS, React Hook Form
**Backend:** Django REST Framework, PostgreSQL, JWT Authentication
**AI Services:** OpenAI GPT-4, Whisper
**Communication:** Twilio Voice API
**Deployment:** Docker, Docker Compose

## Quick Start (Local Development)

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd SmartCallr
```

### 2. Backend Setup (Local)
```bash
cd backend

# Create virtual environment
conda create -n smartcallr-backend python=3.11
conda activate smartcallr-backend

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env  # Add your API keys

# Run migrations
python manage.py migrate

# Start backend
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start frontend
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Alternative: Docker Setup

For Docker deployment (production-like environment):

```bash
cd backend
docker compose up --build
```

See [Docker Setup Guide](backend/README-Docker.md) for details.

## Environment Variables

**Backend (.env):**
```
SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number

# Database (local PostgreSQL)
DB_HOST=localhost
DB_NAME=smartcallr_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_PORT=5432
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
SmartCallr/
├── frontend/          # Next.js React app
├── backend/           # Django REST API
├── README.md         # This file
└── docs/             # Documentation
```

## Key Features

- **Dashboard** - Overview of calls, leads, and metrics
- **Lead Management** - CRUD operations with country code support
- **Call Interface** - Initiate calls, take notes, view transcripts
- **Call History** - Browse past calls with search and filters
- **AI Integration** - Automatic transcription and summarization

## Development Commands

**Backend:**
```bash
conda activate smartcallr-backend
python manage.py runserver          # Start development server
python manage.py migrate            # Run database migrations
python manage.py createsuperuser    # Create admin user
pytest                              # Run tests
```

**Frontend:**
```bash
npm run dev          # Start development server
npm run build        # Production build
npm run lint         # Code linting
npm test             # Run tests
```

## Documentation

- [Docker Setup](backend/README-Docker.md) - For containerized deployment
- [Testing Guide](backend/README-Testing.md) - API testing with pytest
- [Frontend Guide](frontend/README.md) - Next.js app details

## License

MIT License
