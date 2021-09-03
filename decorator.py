from datetime import datetime

from loguru import logger



def timeit(func):
    """
    Декоратор, выводящий время, которое заняло
    выполнение декорируемой функции.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.time()
        res = func(*args, **kwargs)
        logger.info('Функция {funct} выполнена за {duration}', funct=func.__name__, duration=time.time() - t)
        return res
    return wrapper