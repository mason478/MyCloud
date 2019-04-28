from app.commons.cache import RedisConnect

connect = RedisConnect()


def redis_init(app):
    connect.init_app(app)
