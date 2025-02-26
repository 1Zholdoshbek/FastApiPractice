from fastapi import FastAPI
from controllers import router as auth_router

app = FastAPI(title="Система аутентификации", description="API для регистрации и аутентификации пользователей")

# Корневой маршрут
@app.get("/")
def read_root():
    return {
        "message": "Добро пожаловать в API аутентификации",
        "endpoints": {
            "регистрация": "/register",
            "получение токена": "/token",
            "обновление токена": "/refresh_token",
            "профиль": "/users/me",
            "все пользователи": "/users"
        }
    }

# Подключаем роутер
app.include_router(auth_router)

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)