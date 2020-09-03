import logging, os
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

formatter = logging.Formatter("MyCloud:{"
                              "threadName:%(threadName)s,"
                              " asciTime:%(asctime)s,"
                              " levelName:%(levelname)s,"
                              " fileName:%(filename)s,"
                              " funcName:%(funcName)s,"
                              " lineNo:%(lineno)d,"
                              " message: %(message)s}")


class Logger(object):
    """
    日志模块，初始化时从config.py中读取相关的配置
    """
    def __init__(self, app=None):
        self.logger = logging.getLogger()
        if app:
            self.init_app(app)

    def init_app(self, app):
        level = app.config['LOG_LEVEL']
        log_type = app.config["LOG_TYPE"]
        log_path = app.config['LOG_PATH']
        log_name = app.config["LOG_NAME"]
        max_bytes = app.config["LOG_MAX_BYTES"]
        backup_count = app.config["LOG_BACK_UP_COUNT"]

        if level == 'error':
            self.logger.setLevel(logging.ERROR)
        elif level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        if log_type == 'rotate':
            filename = os.path.join(log_path, log_name)
            file_handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
        else:
            file_handler = StreamHandler()
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
