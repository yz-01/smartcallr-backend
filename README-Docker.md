# SmartCallr Backend - Docker Setup

## Quick Start

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Make sure your `.env` file exists** with your actual API keys and database credentials

3. **Build and run with Docker Compose**
   ```bash
   docker compose up --build
   ```

That's it! The container will use your existing local PostgreSQL database.

## Services

- **Backend**: Django API running on http://localhost:8000
- **Database**: Uses your existing local PostgreSQL database

## Useful Commands

```bash
# Stop services
docker compose down

# View logs
docker compose logs backend

# Access backend shell
docker compose exec backend python manage.py shell

# Rebuild and restart
docker compose down
docker compose up --build
```

## Notes

- The container uses `network_mode: "host"` to access your local database
- All configuration is read from your `.env` file
- No need to run migrations again - uses your existing database
- Recordings are mounted from your local `recordings/` folder

## Production Notes

- Change all default passwords and secret keys
- Set DEBUG=False in production
- Use environment-specific configuration files
- Consider using external database services for production 