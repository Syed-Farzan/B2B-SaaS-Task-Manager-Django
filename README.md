# B2B SaaS Task Manager API

A multi-tenant task management backend built with Django, Django REST Framework, PostgreSQL, and JWT authentication.

## Features

- User registration and JWT login
- Organizations and organization memberships
- Admin and member roles
- Projects and tasks
- Organization-level access control
- Django administration panel

## Technology Stack

- Python 3.12+
- Django 6.1
- Django REST Framework 3.18
- djangorestframework-simplejwt 5.5
- PostgreSQL

## Project Structure

```text
B2B SaaS Task Manager-Django/
├── manage.py
├── testy/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
└── tasks/
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd "B2B SaaS Task Manager-Django"
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt psycopg[binary]
```

Create a PostgreSQL database and user:

```sql
CREATE DATABASE taskmanager;
CREATE USER taskmanager_user WITH PASSWORD 'change-this-password';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager_user;
```

Configure these environment variables before starting Django:

```env
POSTGRES_DB=taskmanager
POSTGRES_USER=taskmanager_user
POSTGRES_PASSWORD=change-this-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Configure `DATABASES` in `testy/settings.py`:

```python
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

The API runs at `http://127.0.0.1:8000/`.

The admin panel is available at `http://127.0.0.1:8000/admin/`.

## Authentication

Register or log in to receive an access token. Send the token with protected requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register/` | Register a user |
| POST | `/users/login/` | Receive JWT tokens |
| GET | `/users/me/` | View the current user |

### Organizations

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/organizations/` | List user's organizations |
| POST | `/users/organizations/` | Create an organization |
| GET | `/users/organizations/<uuid>/` | View an organization |
| PATCH | `/users/organizations/<uuid>/` | Update an organization; admin only |
| DELETE | `/users/organizations/<uuid>/` | Delete an organization; admin only |

The user who creates an organization automatically becomes its administrator.

### Memberships

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/memberships/` | List memberships |
| POST | `/users/memberships/` | Add a member; admin only |
| GET | `/users/memberships/<id>/` | View a membership |
| PATCH | `/users/memberships/<id>/` | Update a membership; admin only |
| DELETE | `/users/memberships/<id>/` | Remove a member; admin only |

Roles are `admin` and `member`. The last organization administrator cannot be deleted.

### Projects

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/projects/` | List accessible projects |
| POST | `/users/projects/` | Create a project; admin only |
| GET | `/users/projects/<uuid>/` | View a project |
| PATCH | `/users/projects/<uuid>/` | Update a project; admin only |
| DELETE | `/users/projects/<uuid>/` | Delete a project; admin only |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks/` | List accessible tasks |
| POST | `/tasks/` | Create a task; admin only |
| GET | `/tasks/<uuid>/` | View a task |
| PATCH | `/tasks/<uuid>/` | Update a task; admin only |
| DELETE | `/tasks/<uuid>/` | Delete a task; admin only |

Task statuses are `todo`, `in_progress`, and `done`.

## Example API Requests

### Register

```bash
curl -X POST http://127.0.0.1:8000/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"strong-password"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"strong-password"}'
```

### Create an Organization

```bash
curl -X POST http://127.0.0.1:8000/users/organizations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"name":"Example Company"}'
```

### Create a Project

```bash
curl -X POST http://127.0.0.1:8000/users/projects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"name":"Website Project","description":"Company website","organization":"ORGANIZATION_UUID"}'
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"title":"Design login page","description":"Create the login page","status":"todo","project":"PROJECT_UUID"}'
```

## Data Model

```text
User ── Membership ── Organization ── Project ── Task
```

- A user can belong to multiple organizations.
- An organization can contain multiple projects.
- A project can contain multiple tasks.
- Memberships connect users to organizations and define their roles.

## Testing and Checks

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

Add automated tests before using the project in production.

## Production Security

Before deployment:

- Set `DEBUG = False`.
- Move `SECRET_KEY` into an environment variable.
- Configure `ALLOWED_HOSTS`.
- Use a dedicated PostgreSQL database and database user.
- Enable HTTPS.
- Configure secure cookies and CSRF settings.
- Add rate limiting and password reset functionality.
- Ensure password updates always use Django's `set_password()` method.
- Do not commit `.venv/`, `__pycache__/`, `.env`, or database files.

## Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
.DS_Store
staticfiles/
media/
```

## Future Improvements

- Add task assignment, priorities, and due dates.
- Add pagination and filtering.
- Add Swagger or ReDoc API documentation.
- Add email verification and password reset.
- Add audit logs and organization invitations.
- Add Docker and GitHub Actions configuration.

## License

This project is intended for educational and personal use. Add an open-source license, such as MIT, before commercial distribution.
