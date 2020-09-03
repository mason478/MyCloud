import traceback

from app.commons.change_format import add_response
from app.commons.log_handler import logger


class ErrorRegister:
    def __init__(self, ns, exceptions: list):
        self.ns = ns
        for exception in exceptions:
            self._register(exception)

    def _register(self, exception):
        @self.ns.errorhandler(exception)
        def handle_error(e):
            logger.logger.error("Internal error:{},traceback:{}".format(e, traceback.format_exc()))
            return add_response(r_code=e.error_code), 500
