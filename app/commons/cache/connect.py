import redis

from app.commons.log_handler import logger


# 建立redis 连接池
class RedisConnect:
    def __init__(self):
        self.pool = None

    def init_app(self, app):
        self.pool = redis.ConnectionPool(host=app.config["REDIS_HOST"], password=app.config['REDIS_PASSWORD'],
                                         port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'], socket_timeout=3)
        logger.logger.info('**Init redis connection successfully***')
