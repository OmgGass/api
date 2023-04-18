from flask_sqlalchemy import SQLAlchemy
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig

}

db = SQLAlchemy()
