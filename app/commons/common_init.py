from app.commons.cache import RedisConnect
from app.commons.log_recording import Logger

connect = RedisConnect()
logger = Logger()


def redis_init(app):
    connect.init_app(app)


def logger_init(app):
    logger.init_app(app)
