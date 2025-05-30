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

## Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd SmartCallr
```

### 2. Backend Setup
```bash
cd backend
cp .env.example .env  # Add your API keys
docker compose up --build
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
DB_HOST=host.docker.internal
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

## Development

- **Frontend:** `npm run dev` (localhost:3000)
- **Backend:** `docker compose up` (localhost:8000)
- **Testing:** `pytest` (backend), `npm test` (frontend)

## Documentation

- [Docker Setup](backend/README-Docker.md)
- [Testing Guide](backend/README-Testing.md)
- [Frontend Guide](frontend/README.md)

## License

MIT License
