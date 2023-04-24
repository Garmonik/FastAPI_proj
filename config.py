from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DB_NAME: str | None = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")

    class Config:
        env_file = 'database.env'


settings = Settings()

# from pydantic import BaseSettings
#
#
# class Settings(BaseSettings):
#     DB_NAME: str | None = "test_db"
#     DB_USER: str = "test_user"
#     DB_PASS: str = "test_psw"
#     DB_HOST: str = "localhost"
#     DB_PORT: str = "5432"
#
#     class Config:
#         env_file = 'database.env'
#
#
# settings = Settings()
