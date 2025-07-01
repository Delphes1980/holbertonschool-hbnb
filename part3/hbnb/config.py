import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    ERROR_INCLUDE_MESSAGE = False
    BCRYPT_LOG_ROUNDS = 12

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
