import redis


class RedisConnect:
    def __init__(self):
        self.pool = None

    def init_app(self, app):
        self.pool = redis.ConnectionPool(host=app.config["REDIS_HOST"], password=app.config['REDIS_PASSWORD'],
                                         port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'], socket_timeout=3)
