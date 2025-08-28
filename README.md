# User Management API

A simple user management REST API that I built to learn FastAPI. Handles basic CRUD operations for users with a PostgreSQL database.

## Demo

**Live version:** https://user-management-api-fastapi-production.up.railway.app

Try it out:
- https://user-management-api-fastapi-production.up.railway.app/docs (interactive API docs)
- https://user-management-api-fastapi-production.up.railway.app/health

## What it does

Basic user management - create, view, update, delete users. Has pagination, search, and some simple user stats. Nothing fancy, just a clean API to practice with.

## Stack

- FastAPI (Python web framework)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Docker (for easy setup)
- Railway (hosting)

## Running locally

**Quick start with Docker:**
```bash
git clone https://github.com/your-username/project-1-user-management-api.git
cd project-1-user-management-api
docker-compose up -d
```

Then visit http://localhost:8000/docs

**Manual setup:**
```bash
pip install -r requirements.txt

# You'll need PostgreSQL running
# Default connection: postgresql://postgres:postgres123@localhost:5432/user_management

uvicorn app.main:app --reload
```

## API endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | / | Basic info |
| GET | /health | Health check + DB status |
| POST | /users/ | Create user |
| GET | /users/ | List users (with pagination/search) |
| GET | /users/{id} | Get specific user |
| PUT | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user |
| GET | /users/stats/summary | User count stats |

## Examples

```bash
# Create a user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'

# Get all users
curl "http://localhost:8000/users/"

# Search users
curl "http://localhost:8000/users/?search=test&page=1"
```

## Project structure

```
app/
├── main.py          # Main FastAPI app
├── api/             # Route handlers
├── models/          # Database models  
├── schemas/         # Pydantic models
├── services/        # Business logic
└── core/            # Database + config
```

## Environment variables

For local development, the app uses these defaults:
```
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/user_management
```

Railway automatically provides `DATABASE_URL` and `PORT` for deployment.

## What I learned building this

- FastAPI is really nice for building APIs quickly
- Docker makes local development much easier
- Railway deployment is pretty straightforward
- SQLAlchemy relationships and pagination
- Proper API structure with separate layers

## Things I might add later

- User authentication (JWT probably)
- File uploads for profile pictures
- Email verification
- More detailed user profiles
- Maybe a simple frontend

## Notes

This is a learning project, so the code might not be production-perfect. Feel free to suggest improvements or point out issues!

The database starts empty, so you'll need to create some users first to see anything interesting.