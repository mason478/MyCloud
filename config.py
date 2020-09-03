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
    HOST = 'localhost'
    PORT = 8081

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', "62f4ada291da")
    REDIS_DB = 0

    # log 配置
    LOG_LEVEL = 'debug'  # 日志等级，大于这个等级的日志才会被记录,有:info,debug,error等
    LOG_TYPE = 'steam'  # 是否是轮回日志,rotate:轮回，stream:日志流
    LOG_PATH = os.getcwd()
    LOG_NAME = 'mycloud.log'  # 轮回日志记录的名称
    LOG_MAX_BYTES = 1024 * 1024 * 10
    LOG_BACK_UP_COUNT = 7

    # mysql及连接池的配置
    POOL_MAX_CONNECTION = 10
    POOL_MAX_CACHE = 5
    POOL_MIN_CACHE = 5
    POOL_BLOCKING = True
    DB = 'mycloud'
    DB_USER = 'mason'
    DB_PASSWORD = '1111'
    DB_HOST = 'localhost'
    DB_PORT = 3306


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
