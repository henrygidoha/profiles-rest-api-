# Profiles REST API

A RESTful API built with **Django** and **Django REST Framework** that allows users to create and manage their profiles and post status updates (feed items). The project demonstrates core backend development concepts including custom user authentication, token-based authorization, object-level permissions, and full CRUD operations.

---

## Features

- **User registration & login** — Sign up with email and password, receive an authentication token
- **Custom user model** — Login via email instead of username, with secure password hashing
- **Token authentication** — Stateless auth using DRF's `TokenAuthentication`
- **Profile management** — Create, view, update, and delete user profiles
- **Profile feed** — Authenticated users can post, read, and manage status updates
- **Object-level permissions** — Users can only modify their own profile and feed items
- **Search** — Filter user profiles by name or email via query parameters
- **Browsable API** — Interactive API explorer available in the browser during development

---

## Tech Stack

| Technology | Version | Role |
|---|---|---|
| Python | 3.x | Core language |
| Django | ≥ 4.2 | Web framework (ORM, routing, admin) |
| Django REST Framework | ≥ 3.14 | REST API layer (serializers, viewsets, auth) |
| SQLite3 | Built-in | Development database |

---

## Project Structure

```
profiles-rest-api/
├── profiles_project/          # Django project config
│   ├── settings.py            # Global settings (INSTALLED_APPS, AUTH_USER_MODEL, etc.)
│   ├── urls.py                # Root URL dispatcher
│   └── wsgi.py
│
├── profiles_api/              # Main application
│   ├── models.py              # UserProfile (custom AbstractBaseUser) + ProfileFeedItem
│   ├── serializer.py          # ModelSerializers for each model
│   ├── views.py               # APIView + ModelViewSets
│   ├── permissions.py         # Custom object-level permission classes
│   ├── urls.py                # App-level URLs + DefaultRouter
│   ├── admin.py               # Admin panel registration
│   └── migrations/            # Database schema history
│
├── manage.py
└── requirement.txt
```

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/api/login/` | No | Obtain authentication token |
| `GET` | `/api/user-profiles/` | No | List all user profiles |
| `POST` | `/api/user-profiles/` | No | Register a new user |
| `GET` | `/api/user-profiles/{id}/` | No | Retrieve a profile |
| `PUT` | `/api/user-profiles/{id}/` | Yes (owner) | Full update of own profile |
| `PATCH` | `/api/user-profiles/{id}/` | Yes (owner) | Partial update of own profile |
| `DELETE` | `/api/user-profiles/{id}/` | Yes (owner) | Delete own profile |
| `GET` | `/api/profile-feed/` | Yes | List all feed items |
| `POST` | `/api/profile-feed/` | Yes | Create a new status update |
| `GET` | `/api/profile-feed/{id}/` | Yes | Retrieve a feed item |
| `PUT` | `/api/profile-feed/{id}/` | Yes (owner) | Update own feed item |
| `PATCH` | `/api/profile-feed/{id}/` | Yes (owner) | Partially update own feed item |
| `DELETE` | `/api/profile-feed/{id}/` | Yes (owner) | Delete own feed item |

**Search:** `GET /api/user-profiles/?search=<query>` — searches across `name` and `email` fields.

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/henrygidoha/profiles-rest-api-.git
cd profiles-rest-api-

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirement.txt

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create an admin superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.
The admin panel is at `http://127.0.0.1:8000/admin/`.

---

## Authentication Flow

```
1. Register   POST /api/user-profiles/   { "email": "...", "name": "...", "password": "..." }
2. Login      POST /api/login/           { "username": "email@example.com", "password": "..." }
              ← Response: { "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4" }
3. Use token  Add header to every request:
              Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4
```

---

## Key Design Decisions

**Custom User Model** — The project replaces Django's default `User` with a custom `UserProfile` using `AbstractBaseUser`. This enables email-based login and makes the user model easily extensible for future fields. This is a best practice that must be done at project start before the first migration.

**Object-Level Permissions** — Two custom `BasePermission` classes (`UpdateOwnProfile`, `UpdateOwnStatus`) ensure that read operations are open to all while write operations (PUT, PATCH, DELETE) are restricted to the resource owner.

**Token Authentication** — Stateless token auth means no server-side sessions. The client stores and sends the token with each request, making the API horizontally scalable.

**`perform_create()` override** — In `UserProfileFeedViewSet`, `user_profile` is automatically set to the authenticated user on the server side. The field is read-only in the serializer to prevent clients from impersonating other users.

---

## Development Notes

- The database file `db.sqlite3` is excluded from version control.
- `SECRET_KEY` should be loaded from an environment variable in production — never hardcoded.
- SQLite is used for development. For production, switch to PostgreSQL.

---

## License

This project is licensed under the terms found in the [LISCENSE](./LISCENSE) file.