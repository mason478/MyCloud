import pymysql
from DBUtils.PooledDB import PooledDB

from app.commons.log_handler import logger


class SqlConnect:
    """建立连接池"""

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, app=None):
        self.pool = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.pool = PooledDB(pymysql, maxconnections=app.config['POOL_MAX_CONNECTION'],
                             maxcached=app.config['POOL_MAX_CACHE'],
                             mincached=app.config['POOL_MIN_CACHE'],
                             blocking=app.config['POOL_BLOCKING'],
                             db=app.config['DB'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                             host=app.config['DB_HOST'], port=app.config['DB_PORT'],
                             cursorclass=pymysql.cursors.DictCursor)
        logger.logger.info("***Init mysql database successfully.***")
