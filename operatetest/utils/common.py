import datetime
import os

__all__ = ["screenshort"]


def screenshort(d):
    """截图,并保存,返回路径"""
    img_path = os.path.join(r"D:\dev\autotest_device\report", "{}.png".format(get_time_stamp()))
    d.screenshot(img_path)
    return img_path


def get_time_stamp():
    """获取时间戳"""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
