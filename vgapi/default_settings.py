import os

class BaseAppConfig(object):

    SQLALCHEMY_DATABASE_URI="postgresql://{}:{}@{}:{}/{}".format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME'],
    )

    API_VERSION = 1.0

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = 'test'
    LOG_DEFAULT_EXCEPTIONS = False

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    ERROR_404_HELP = False
    LOG_FILE = 'messages.log'
    SERVER_LOG_FILE = 'server.log'

class ProductionConfig(BaseAppConfig):
    RESTPLUS_MASK_SWAGGER = True

class StagingConfig(BaseAppConfig):
    pass

class DevConfig(BaseAppConfig):
    pass
