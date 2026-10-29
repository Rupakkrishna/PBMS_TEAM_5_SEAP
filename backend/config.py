import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "pbrms-dev-secret-key-2026")
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))
    JWT_EXPIRATION = timedelta(hours=JWT_EXPIRY_HOURS)
    
    # Database Settings (MySQL 8 with PyMySQL)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "pbrms_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "pbrms_db")
    USE_SQLITE_FALLBACK = os.getenv("USE_SQLITE_FALLBACK", "false").lower() == "true"
    SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pbrms_dev.sqlite")
    
    # Business logic defaults
    MIN_RENTAL_HOURS = 1.0  # Minimum 1 hour billable duration
    DEFAULT_PAGE_SIZE = 50
    
    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }
    
    # Safe URI creation with password encoding
    _encoded_pwd = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    _mysql_uri = f"mysql+pymysql://{DB_USER}:{_encoded_pwd}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    _sqlite_uri = f"sqlite:///{os.path.abspath(SQLITE_DB_PATH).replace('\\', '/')}"
    
    SQLALCHEMY_DATABASE_URI = _sqlite_uri if USE_SQLITE_FALLBACK else _mysql_uri

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration with dedicated test database / SQLite support."""
    DEBUG = True
    TESTING = True
    DB_NAME = os.getenv("TEST_DB_NAME", "pbrms_test_db")
    USE_SQLITE_TEST = os.getenv("USE_SQLITE_TEST", "true").lower() == "true"
    SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pbrms_test.sqlite")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(SQLITE_DB_PATH).replace('\\', '/')}"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
