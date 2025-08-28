# User Management API

Simple REST API for user management built with FastAPI and PostgreSQL.

## What it does

This API handles basic user operations - creating, reading, updating, and deleting user accounts. I built it to learn FastAPI fundamentals and practice building clean APIs.

## Tech Stack

- FastAPI for the web framework
- PostgreSQL for data storage
- SQLAlchemy as the ORM
- Docker for containerization
- Pydantic for data validation

## Getting Started

### With Docker (recommended)
```bash
git clone <repo-url>
cd project-1-user-management-api
docker-compose up -d
```

The API will be available at `http://localhost:8000` and docs at `http://localhost:8000/docs`.

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL required)
cp .env.example .env
# Edit .env with your database URL

# Run the application
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /users` - Create a new user
- `GET /users` - List all users (with pagination)
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user
- `GET /health` - Health check

## Project Structure

```
app/
├── main.py          # FastAPI application
├── models/          # Database models
├── schemas/         # Pydantic schemas
├── api/            # API endpoints
├── core/           # Database and config
└── services/       # Business logic
```

## What I learned

- FastAPI basics and automatic API documentation
- SQLAlchemy ORM patterns
- Database migrations with Alembic
- Docker containerization
- API design principles

## Future improvements

- Add authentication
- Implement file uploads
- Add email notifications
- Better error handling
- API rate limiting