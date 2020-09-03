from app.commons.cache import RedisConnect
from app.commons.db_utils.connect import SqlConnect
# from app.commons.db_utils import SqlConnect

connect = RedisConnect()
sql_connect = SqlConnect()


# def redis_init(app):
#     connect.init_app(app)
#
#
# def sql_init(app):
#     sql_connect.init_app(app)

def init_function(app):
    for obj in (connect, sql_connect):
        obj.init_app(app)
