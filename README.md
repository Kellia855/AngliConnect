# Church Management System

A Django-based web application for managing church members, sacramental records (baptism, confirmation, marriage), roles, and certificate verification.

---

## Requirements

- Python 3.10+
- pip

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd church_system
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the development server

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**

---

## Accessing the System

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home / landing page |
| `http://127.0.0.1:8000/login/` | Login page |
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://127.0.0.1:8000/dashboard/` | Staff dashboard (staff/admin only) |
| `http://127.0.0.1:8000/portal/` | Member portal (members only) |

- **Staff/Admin** users are redirected to the dashboard after login.
- **Church members** with a linked user account are redirected to the member portal after login.

---

## Management Commands

### Create a user account for a church member

```bash
python manage.py create_member_account <member_id> <username> --password <password>
```

**Example:**
```bash
python manage.py create_member_account 1 john.doe --password secret123
```

If `--password` is omitted, the default password is `changeme123`.

### Assign default "Church Member" role to members without any role

```bash
python manage.py assign_default_member_roles
```

---

## Project Structure

```
church_system/
├── manage.py
├── requirements.txt
├── db.sqlite3               # SQLite database (auto-created)
├── church/                  # Main app (models, views, forms, etc.)
│   └── management/
│       └── commands/        # Custom management commands
├── church_config/           # Django project settings & URLs
├── templates/               # HTML templates
├── static/                  # CSS and static assets
└── media/                   # Uploaded files (e.g., member photos)
```

---

## Key Features

- Member registration and profile management (with photo upload)
- Sacramental records: Baptism, Confirmation, Marriage
- Role management and assignment
- Certificate generation and QR-code verification
- Member self-service portal (view profile, change password)
- Staff dashboard for full administration

---

## Notes

- The database used is **SQLite** (`db.sqlite3`), stored in the project root. No additional database setup is required for development.
- Media files (member photos) are stored in the `media/` directory.
- Debug mode is **on** by default — do not use this configuration in production.
- For production deployment, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and use a secure `SECRET_KEY` in `settings.py`.
