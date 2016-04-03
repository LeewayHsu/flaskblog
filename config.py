#!flask/bin/python

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'perhaps-kid'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskblog:123456@localhost/flaskblog?charset=utf8"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskblog:123456@localhost/flaskblog?charset=utf8"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://flaskblog:123456@localhost/flaskblog?charset=utf8"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
#CSRF_ENABLED = True



