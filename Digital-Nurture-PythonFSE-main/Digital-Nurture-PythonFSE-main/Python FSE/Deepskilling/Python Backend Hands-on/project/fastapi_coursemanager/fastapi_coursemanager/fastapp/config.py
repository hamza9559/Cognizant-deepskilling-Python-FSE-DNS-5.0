class Settings:
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./fastapi_courses.db"

settings = Settings()