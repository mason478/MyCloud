from app.commons.log_handler.log_recording import Logger

logger = Logger()


def logger_init(app):
    logger.init_app(app)