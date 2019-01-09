class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:280294@localhost/flaskmovie'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = False