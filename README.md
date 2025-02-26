# FastAPI Authentication System

<div align="center">
  
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

</div>

<p align="center">A robust API system for user registration and authentication using FastAPI and PostgreSQL</p>

## 📋 Features

- User registration with email verification
- JWT-based authentication with access and refresh tokens
- Secure password hashing with bcrypt
- Role-based access control
- PostgreSQL database integration
- Alembic migrations support
- Comprehensive API documentation with Swagger UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/1Zholdoshbek/FastApiPractice.git
cd FastApiPractice
```

2. **Create and activate virtual environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/MacOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

1. **Ensure PostgreSQL is installed and running**

2. **Create a database**

```sql
CREATE DATABASE fastapi;
```

3. **Configure connection string**

Edit `alembic.ini` and update the database connection string:

```ini
# For async connection (recommended)
sqlalchemy.url = postgresql+asyncpg://your_username:your_password@localhost/fastapi

# OR for sync connection
# sqlalchemy.url = postgresql+psycopg2://your_username:your_password@localhost/fastapi
```

4. **Run migrations**

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🏃‍♂️ Running the Application

1. **Start the server**

```bash
uvicorn main:app --reload
```

2. **Access the API documentation**

Open your browser and navigate to:
```
http://127.0.0.1:8000/docs
```

## 📡 API Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/` | Root route with API information | No |
| POST | `/register` | Register a new user | No |
| POST | `/token` | Get access and refresh tokens | No |
| POST | `/refresh_token` | Refresh access token | No |
| GET | `/users/me` | Get current user information | Yes |
| GET | `/users` | Get all users (demo purposes) | Yes |

## 📝 Usage Examples

### Register a new user

```http
POST http://127.0.0.1:8000/register
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword",
    "full_name": "Test User"
}
```

### Get authentication tokens

```http
POST http://127.0.0.1:8000/token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=testpassword
```

### Refresh token

```http
POST http://127.0.0.1:8000/refresh_token
Content-Type: application/json

{
    "refresh_token": "your-refresh-token"
}
```

### Get current user info

```http
GET http://127.0.0.1:8000/users/me
Authorization: Bearer your-access-token
```

### Get all users

```http
GET http://127.0.0.1:8000/users
Authorization: Bearer your-access-token
```

## 📦 Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **SQLAlchemy**: ORM for database operations
- **asyncpg**: Async PostgreSQL driver
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **bcrypt**: Password encryption
- **Alembic**: Database migrations


## 🔒 Security

- Passwords are hashed using bcrypt
- Authentication is handled via JWT tokens
- Refresh tokens with limited lifetime
- Input validation using Pydantic



## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request