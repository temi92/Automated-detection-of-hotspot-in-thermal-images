import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
