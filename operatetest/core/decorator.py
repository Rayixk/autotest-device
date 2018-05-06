import os
import re
import datetime
import functools
from ..auxiliary import VAR


from .uiautomator import UIAutomatorServer


__all__ = ["keyword"]
import inspect

def keyword(func):
    @functools.wraps(func)
    def inner(ad,*args, **kwargs):

        name = func.__name__
        res = func(ad,*args, **kwargs)

        curr_line = inspect.stack()[1][4][0].strip().strip("\n")

        _record_screenshot(ad, name, curr_line)

        return res

    return inner


def _record_screenshot(ad, func_name, curr_line):
    """截图和记录log"""

    if isinstance(ad,UIAutomatorServer):
        img_path = screenshort(ad)
        ad.log.info(img_path)

    #确保记录的log不包含不应该包含的内容
    ret = re.search(r'{}.*?\)+'.format(func_name), curr_line)
    if ret:
        t = ret.group(0)
        a, b = curr_line.split(t)
        ad.log.info("".join([a, t]))



def screenshort(d):
    """截图,并保存,返回路径"""
    time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    img_path = os.path.join(VAR.screenshoot_dir, "{}.png".format(time_stamp))
    d.screenshot(img_path)
    return img_path
