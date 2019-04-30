# 为了避免循环导入错误，logger 的初始化不放在common_init模块
from app.commons.log_handler.log_recording import Logger

logger = Logger()


def logger_init(app):
    logger.init_app(app)