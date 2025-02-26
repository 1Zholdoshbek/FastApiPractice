from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import UserInDB, TokenData

# Настройки
SECRET_KEY = "your-secret-key"  # Замените на свой секретный ключ
ALGORITHM = "HS256"  # Алгоритм шифрования
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни access token
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Время жизни refresh token

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Расширенная база данных пользователей
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "disabled": False,
        "hashed_password": pwd_context.hash("secret"),  # Пароль "secret" захеширован
    }
}


# Функция для хеширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция для получения пользователя из базы данных
def get_user(db: dict, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def create_user(db: dict, username: str, email: str, password: str, full_name: Optional[str] = None) -> Optional[UserInDB]:
    if username in db:
        raise ValueError("Пользователь с таким именем уже существует")  # Явное исключение
    hashed_password = get_password_hash(password)
    user_data = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "disabled": False,
        "hashed_password": hashed_password
    }
    db[username] = user_data
    return UserInDB(**user_data)


# Функция для аутентификации пользователя
def authenticate_user(db: dict, username: str, password: str) -> Optional[UserInDB]:
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Функция для создания access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для создания refresh token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt