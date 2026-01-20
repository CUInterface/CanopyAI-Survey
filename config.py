import os
from pathlib import Path

basedir = Path(__file__).parent.absolute()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir / "instance" / "survey.db"}'


class ProductionConfig(Config):
    DEBUG = False
    # Use DATABASE_PATH env var for Azure Files mount, fallback to instance folder
    _db_path = os.environ.get('DATABASE_PATH') or str(basedir / "instance" / "survey.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{_db_path}'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
