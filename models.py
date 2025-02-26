from typing import Optional
from pydantic import BaseModel
# Модель пользователя с дополнительными полями
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# Модель для хранения пароля (для базы данных)
class UserInDB(User):
    hashed_password: str

# Модель запроса для создания пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

# Модель токена
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

# Модель данных в токене
class TokenData(BaseModel):
    username: Optional[str] = None

# Модель для обновления refresh-токена
class RefreshTokenRequest(BaseModel):
    refresh_token: str