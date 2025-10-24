# VOA Secrets Manager API

A secure and robust API for managing secrets, users, and audits. Built with **FastAPI**, **SQLAlchemy**, **Alembic**, and Docker-ready for deployment.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Database Initialization](#database-initialization)
- [Running the API](#running-the-api)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- User management (Admin & Developer roles)
- Secrets management
- Audit logging
- Secure password hashing
- Dockerized for easy deployment
- Alembic migrations for database version control

---

## Project Structure

```
backend/
├─ alembic/               # Database migrations
├─ app/
│  ├─ api/                # API routes
│  ├─ core/               # Core configurations and database
│  ├─ dependencies/       # Dependency injections
│  ├─ models/             # SQLAlchemy models
│  ├─ schemas/            # Pydantic schemas
│  ├─ services/           # Business logic
│  └─ utils/              # Utility functions (logging, helpers, etc.)
├─ tests/                 # Unit tests / Postman collections
├─ Dockerfile
├─ start.sh               # Script to run migrations & start server
├─ requirements.txt
├─ db_test.py             # Script to create initial users
└─ alembic.ini
```

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/senani-derradji/VOA
cd VOA/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env to include your configuration
```

---

## Docker Deployment

1. Build Docker image:
```bash
docker build -t voa-backend .
```

2. Run container:
```bash
docker run -d -p 8000:8000 --name voa-backend voa-backend
```

The API will be accessible at `http://localhost:8000`.

---

## Database Initialization

The `start.sh` script runs Alembic migrations and initializes default users (`admin` & `developer`) using `db_test.py`:

**Default credentials:**
```
Admin:
  username: adminderradji
  password: Admin@PassWord.1+1

Developer:
  username: devinderradji
  password: Dev@PassWord.1+1
```

> Make sure to change these passwords in production.

---

## Environment Variables

Create a `.env` file with at least the following variables:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your_secret_key
```
**OR**
```python
python VOA/install.py
``` 

---

## Testing

- **Pytest:**  
```bash
pytest -v
```

- **Postman:**  
The `tests/postman/` directory contains collections for testing the API endpoints.
cd tests/postman/ && newman run admin_test -e admin_env
cd tests/postman/ && newman run dev_test -e dev_env
```

---