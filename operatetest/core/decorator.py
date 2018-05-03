import functools

from ..utils.log import Logger
from ..utils import common

log = Logger.get_logger("__report__")

__all__ = ["keyword"]
import inspect

def keyword(func):
    @functools.wraps(func)
    def inner(ad,*args, **kwargs):

        name = func.__name__
        res = func(ad,*args, **kwargs)

        curr_line = inspect.stack()[1][4][0].strip().strip("\n")
        log.info(curr_line)
        img_path = common.screen_short(ad)
        log.info(img_path)
        return res

    return inner
