# Task Management API

A secure and structured REST API for managing users, projects, and tasks, built with FastAPI and PostgreSQL.

This project was created as a backend portfolio project with a focus on authentication, authorization, database design, API security, and clean project structure.

## Features

* User registration
* User login
* JWT authentication
* Argon2 password hashing
* Project CRUD operations
* Task CRUD operations
* User-based authorization
* IDOR protection
* Input validation with Pydantic
* SQL injection protection through SQLAlchemy ORM
* Rate limiting on login requests
* Secure error handling
* Application logging
* PostgreSQL database
* Database migrations with Alembic

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* python-jose
* Argon2
* SlowAPI
* Uvicorn

## Project Structure

```text
Task managment api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── dependencies.py
│   ├── limiter.py
│   └── routes/
│       ├── auth.py
│       ├── users.py
│       ├── projects.py
│       └── tasks.py
│
├── alembic/
├── alembic.ini
├── logging_config.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Security

This project includes several practical backend security protections.

### Authentication

Users authenticate using JWT access tokens.

Protected endpoints require:

```http
Authorization: Bearer <token>
```

### Password Security

Passwords are never stored in plain text.

They are hashed using Argon2 before being stored in the database.

### Authorization

Users can only access projects that belong to their own account.

Tasks are also protected through their parent project ownership.

This prevents unauthorized access and IDOR vulnerabilities.

### Input Validation

Request data is validated using Pydantic schemas.

Invalid request types or formats return validation errors.

### SQL Injection Protection

Database operations are performed using SQLAlchemy ORM instead of manually constructing SQL queries.

### Rate Limiting

Login attempts are rate-limited to reduce brute-force attacks.

Current login limit:

```text
5 requests per minute
```

### Secure Error Handling

Internal database errors are not directly exposed to API users.

Database transactions use rollback when an operation fails.

### Logging

Important application and security events are logged, including:

* Successful login
* Failed login attempts
* Project creation
* Project updates
* Project deletion
* Task creation
* Task updates
* Task deletion
* Unauthorized access attempts
* Database errors

Sensitive information such as passwords and JWT tokens is not logged.

## Database Models

### User

```text
id
username
password_hash
```

### Project

```text
id
name
description
user_id
```

### Task

```text
id
name
description
status
priority
deadline
project_id
```

Relationships:

```text
User
 └── Projects
      └── Tasks
```

## API Endpoints

### Authentication

```http
POST /register
POST /login
```

### Projects

```http
POST   /projects
GET    /projects
GET    /projects/{project_id}
PUT    /projects/{project_id}
DELETE /projects/{project_id}
```

### Tasks

```http
POST   /projects/{project_id}/tasks
GET    /projects/{project_id}/tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
```

## Installation

Clone the repository:

```bash
git clone https://github.com/shayantokhmechi6-sys/task-management-api.git
```

Enter the project directory:

```bash
cd task-management-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory.

Example:

```env
SECRET_KEY=your-secret-key
```

Do not commit the `.env` file to GitHub.

## PostgreSQL

Make sure PostgreSQL is running and create the project database.

The current application configuration expects a PostgreSQL database connection.

Update the connection string in `app/database.py` if your PostgreSQL username, password, port, host, or database name is different.

Example format:

```text
postgresql+psycopg://username:password@localhost:5432/database_name
```

## Database Migrations

Alembic is used to manage database schema migrations.

Check the current migration:

```bash
alembic current
```

Apply migrations:

```bash
alembic upgrade head
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

The API was manually tested using Postman.

Tests included:

* Successful registration
* Duplicate username handling
* Successful login
* Invalid login credentials
* Invalid JWT
* Expired or malformed authentication tokens
* Project CRUD operations
* Task CRUD operations
* Unauthorized project access
* Unauthorized task access
* IDOR attempts
* Invalid input types
* SQL injection attempts
* Rate limiting
* Database error handling
* Application logging

## Purpose

This project was developed as a backend portfolio project to practice and demonstrate:

* REST API development
* Backend architecture
* Relational database design
* Authentication
* Authorization
* API security
* PostgreSQL
* SQLAlchemy ORM
* Database migrations
* Error handling
* Logging
* Git and GitHub workflow

## Author

**Shayan Tokhmechi**
