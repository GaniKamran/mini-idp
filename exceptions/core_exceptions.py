import logging
import traceback
from datetime import datetime

# Loq qurulumu
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app_errors.log",  # log faylı
    filemode="a"
)


class AppException(Exception):
    """Baza exception sinifi - bütün custom exception-lar buradan miras alacaq"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class BadRequestException(AppException):
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)


class ExceptionHandler:
    """Exception idarəedici sinif"""
    def handle(self, ex: Exception):
        if isinstance(ex, AppException):
            self._log_exception(ex)
            return {
                "error": ex.message,
                "status_code": ex.status_code,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            self._log_exception(ex, is_unexpected=True)
            return {
                "error": "Internal server error",
                "status_code": 500,
                "timestamp": datetime.utcnow().isoformat()
            }

    def _log_exception(self, ex: Exception, is_unexpected=False):
        if is_unexpected:
            logging.error("Unexpected Error: %s\n%s", str(ex), traceback.format_exc())
        else:
            logging.warning("Handled Exception: %s", str(ex))
