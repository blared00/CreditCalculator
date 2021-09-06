import time

from loguru import logger


def catch_raise(func):
    """Декоратор для отлавливания исключений и их логирование"""

    def catch(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.debug(e)
            raise e

    return catch


def timeit(func):
    """Декоратора для замера времени работы функции"""

    def timer(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        delta = (time.time() - ts) * 1000
        logger.info(f"{func.__name__} выполнялся {delta:2.2f} ms")
        return result

    return timer
