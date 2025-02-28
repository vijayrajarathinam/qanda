class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = 'b3471d1a-993e-11eb-bacf-3bc0a276fa06'
    BCRYPT_LOG_ROUTES = 4
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    SQLALCHEMY_DATABASE_URI = 'sqlite:////opt/app/app.db'

class DevelopmentConfig(BaseConfig):
    """ Development Config """
    pass

class TestingConfig(BaseConfig):
    """ Testing Config """
    pass

class ProductionConfig(BaseConfig):
    """ Development Config """
    pass
