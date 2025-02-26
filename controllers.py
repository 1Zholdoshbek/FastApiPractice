from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from models import Token, User, UserInDB, TokenData, UserCreate, RefreshTokenRequest
from services import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    fake_users_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    ALGORITHM,
    get_user,
    create_user
)
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Эндпоинт для регистрации нового пользователя
@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    try:
        existing_user = get_user(fake_users_db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )
        user = create_user(
            fake_users_db,
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.full_name
        )
        user_response = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=user.disabled
        )
        return user_response
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при регистрации пользователя"
        )

# Эндпоинт для получения токенов
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


# Эндпоинт для обновления access token
@router.post("/refresh_token", response_model=Token)
async def refresh_token(request: RefreshTokenRequest):
    refresh_token = request.refresh_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


# Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Функция для получения активного пользователя
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


# Эндпоинт для получения профиля текущего пользователя
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user


# Эндпоинт для получения всех пользователей (только для демонстрации)
@router.get("/users", response_model=list[User])
async def read_all_users(current_user: UserInDB = Depends(get_current_active_user)):
    # В реальном приложении здесь должна быть проверка прав администратора
    users = []
    for username, user_data in fake_users_db.items():
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data.get("full_name"),
            disabled=user_data.get("disabled", False)
        )
        users.append(user)
    return users