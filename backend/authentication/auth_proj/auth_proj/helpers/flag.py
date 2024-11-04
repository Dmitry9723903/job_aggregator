import logging
from django.core.cache import cache
from functools import wraps

from .constants import TASK_SKIPPED

logger = logging.getLogger(__name__)


class Flag(object):
    """
    Флаг на основе Django-кэша
    """

    def __init__(self, timeout=60, **kwargs):
        self.timeout = timeout
        self.key = str(kwargs)

    def set(self):
        if not self.get():
            logger.debug(f"Устанавливаем флаг {self}...")
            return cache.set(self.key, "flagged", self.timeout)
        else:
            return False

    def get(self):
        return cache.get(self.key)

    def delete(self):
        logger.debug(f"Удаляем флаг {self}...")
        return cache.delete(self.key)

    def __str__(self):
        return f"Flag {self.key} for {self.timeout} seconds"


def tasklock_cleaner_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _flag = Flag(
            task=func.__name__,
            apikey_id=kwargs.get("apikey_id"),
        )
        _flag_executor = Flag(
            task=f"executor_{func.__name__}",
            apikey_id=kwargs.get("apikey_id"),
            timeout=60 * 60 * 6,  # блокируем на 6 часов
        )
        if _flag_executor.set():
            try:
                result = func(*args, **kwargs)
            finally:
                _flag.delete()
                _flag_executor.delete()
        else:
            msg = f"Обнаружен флаг выполнения задачи {_flag_executor}. Выходим..."
            result = {TASK_SKIPPED: msg}

        return result

    return wrapper
