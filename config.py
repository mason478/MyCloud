import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    @classmethod
    def start_hook(cls):
        pass

    @classmethod
    def init_app(cls, app):
        pass


class LocalmachineConfig(Config):
    DEBUG = True
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD=os.getenv('REDIS_PASSWORD',"62f4ada291da")
    REDIS_DB = 0




class TestingConfig(Config):
    DEBUG = True
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0


class ProductionConfig(Config):
    DEBUG = False



class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)


config = {
    'development': LocalmachineConfig,
    'testing': TestingConfig,
    'production': DockerConfig,
    'default': LocalmachineConfig
}