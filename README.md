# Task Management API

A RESTful API for managing personal or team tasks, built with Django and Django REST Framework (DRF). Users can register, log in with JWT authentication, and perform CRUD operations on tasks (create, read, update, delete), including marking tasks as complete/incomplete. The API supports task ownership, filtering by status or due date, and is extensible for features like categories, reminders, or integrations (e.g., Google Calendar, SendGrid). Deployed to Render or PythonAnywhere for production use.

**Tech Stack**:
- Django 5.1+
- Django REST Framework 3.15
- djangorestframework-simplejwt 5.3 (JWT authentication)
- SQLite (local development) / PostgreSQL (production, Render)
- Deployment: Render (primary) or PythonAnywhere
- Optional: SendGrid for email reminders (post-MVP)

# Features
- Secure JWT-based authentication
- CRUD operations for user-specific tasks
- Filter by status (completed / pending) or due date (today)
- Task categories (optional)
- Fully ready for production deployment

**Database Schema**:
   # User
     | Field    | Type   | Notes          |
     | -------- | ------ | -------------- |
     | id       | PK     | Auto-generated |
     | username | string | Unique         |
     | email    | string | Unique         |
     | password | string | Hashed         |

   # Task
     | Field                   | Type      | Notes             |
  | ----------------------- | --------- | ----------------- |
  | id                      | PK        | Auto-generated    |
  | title                   | string    | Required          |
  | description             | text      | Optional          |
  | status                  | string    | pending/completed |
  | priority                | string    | Low/Medium/High   |
  | due_date                | date      | Optional          |
  | owner                   | FK (User) | Linked to user    |
  | created_at / updated_at | datetime  | Auto timestamps   |

# Endpoint
  # Auth
   | Method | Endpoint              | Description          |
 | ------ | --------------------- | -------------------- |
 | `POST` | `/api/auth/register/` | Register user        |
 | `POST` | `/api/auth/login/`    | Login, get JWT token |

 # Tasks
 | Method           | Endpoint                    | Description                  |
| ---------------- | --------------------------- | ---------------------------- |
| `GET/POST`       | `/api/tasks/`               | List or create tasks         |
| `GET/PUT/DELETE` | `/api/tasks/<id>/`          | View, edit, or delete a task |
| `PATCH`          | `/api/tasks/<id>/complete/` | Toggle task completion       |
| `GET/POST`       | `/api/tasks/categories/`    | Manage categories            |
