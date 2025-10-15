# Task Management API

A RESTful API for managing personal or team tasks, built with Django and Django REST Framework (DRF). Users can register, log in with JWT authentication, and perform CRUD operations on tasks (create, read, update, delete), including marking tasks as complete/incomplete. The API supports task ownership, filtering by status or due date, and is extensible for features like categories, reminders, or integrations (e.g., Google Calendar, SendGrid). Deployed to Render or PythonAnywhere for production use.

**Tech Stack**:
- Django 5.1+
- Django REST Framework 3.15
- djangorestframework-simplejwt 5.3 (JWT authentication)
- SQLite (local development) / PostgreSQL (production, Render)
- Deployment: Render (primary) or PythonAnywhere
- Optional: SendGrid for email reminders (post-MVP)

## Project Overview
The Task Management API enables users to:
- Register and log in securely with JWT tokens.
- Manage personal tasks (create, read, update, delete).
- Mark tasks as complete/incomplete.
- Filter tasks by status (`completed`/`pending`) or due date (`today`).
- Ensure tasks are user-specific (via `owner` foreign key).
- Deploy to a production environment (Render/PythonAnywhere).

**Database Schema**:
- **User** (`CustomUser`):
  - `id` (PK, auto-generated)
  - `username` (string, unique)
  - `email` (string, unique)
  - `password` (hashed)
  - `first_name`, `last_name` (optional)
- **Task**:
  - `id` (PK, auto-generated)
  - `title` (string, max 200)
  - `description` (text, optional)
  - `status` (boolean, default=False)
  - `due_date` (date, optional)
  - `owner` (ForeignKey to `CustomUser`)
  - `created_at`, `updated_at` (timestamps)

**Entity Relationship**: One `CustomUser` to many `Task` (1:M via `owner`).

## Project Progress

- ✅ Initialized Django project (`taskmanager`) and Git repository.
- ✅ Set up virtual environment with dependencies (Django, DRF, JWT, Heroku tools).
- ✅ Created apps: `users` (auth/profile) and `tasks` (task management).
- ✅ Defined models: `CustomUser` (extends `AbstractUser`) and `Task`.
- ✅ Applied migrations (SQLite locally).
- ✅ Tested admin panel with superuser.
- ✅ Implemented JWT-based authentication:
  - `POST /api/users/register/`: Register new users.
  - `POST /api/users/login/`: Log in, get JWT tokens.
  - `GET/PUT /api/users/profile/`: View/update profile.
- ✅ Secured endpoints with `IsAuthenticated` (except register/login).
- ✅ Tested auth endpoints via curl/Postman.
- ✅ Added task CRUD endpoints:
  - `POST /api/tasks/`: Create task.
  - `GET /api/tasks/`: List user’s tasks.
  - `GET/PUT/DELETE /api/tasks/<id>/`: Task details, update, delete.
  - `PATCH /api/tasks/<id>/complete/`: Toggle task status.
- ✅ Ensured tasks are user-specific (via `owner`).
- ✅ Wrote basic tests for task endpoints.
- ✅ Added filtering to `GET /api/tasks/`:
  - `?status=completed` or `?status=pending`.
  - `?due_date=today`.
- ✅ Improved error handling (e.g., 404 for invalid task IDs).
- ✅ Added custom permissions (only owners access their tasks).
- ✅ Optimized API responses (e.g., minimal fields in list view).
- ✅ Wrote comprehensive API documentation (endpoint table, examples).
- ✅ Added test suite with ~80% coverage (using `coverage`).
- ✅ Deployed to Heroku (or PythonAnywhere).
- ✅ Configured production settings (PostgreSQL, static files via WhiteNoise).
- ✅ Optional: Planned SendGrid integration for reminders (post-MVP).




