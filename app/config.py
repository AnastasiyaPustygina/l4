import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/user_manager_db?client_encoding=UTF8"
    CSRF_ENABLED = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/test_db?client_encoding=UTF8"
    TESTING = True
    SECRET_KEY = "supersecretkey"
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

