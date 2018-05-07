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
        curr_line = inspect.stack()[1][4][0].strip().strip("\n")

        # 确保记录的log不包含不应该包含的内容
        ret = re.search(r'{}.*?\)+'.format(name), curr_line)
        if ret:
            t = ret.group(0)
            a, b = curr_line.split(t)
            ad.log.info("".join([a, t]), keyword=True)

        res = func(ad, *args, **kwargs)

        _screenshot(ad)

        return res

    return inner


def _screenshot(ad):
    """截图"""

    if VAR.screen_shot == "true":
        if isinstance(ad,UIAutomatorServer):
            img_path = screenshort(ad)
            ad.log.debug(img_path,img_path=True)



def screenshort(d):
    """截图,并保存,返回路径"""
    time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    img_path = os.path.join(VAR.screen_shot_dir, "{}.png".format(time_stamp))
    d.screenshot(img_path)
    return img_path
