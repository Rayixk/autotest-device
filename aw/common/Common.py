# Created by yang

import time

from operatetest import keyword


@keyword
def sleep(n):
    time.sleep(n)


@keyword
def touchByText(ad, text):
    """
    根据文本点击
    :param ad: 
    :param text: 
    :return: 
    """
    ad(text=text).click()


@keyword
def touchByDesc(ad, desc):
    """
    根据描述点击
    :param ad: 
    :param desc: 
    :return: 
    """
    ad(description=desc).click()


@keyword
def launchApp(ad, pkgname, wait=3):
    """
    启动app
    :param ad: 
    :param pkgname: app 包名
    :param wait: 等待时间
    :return: 
    """
    ad.app_start(pkgname)
    time.sleep(wait) if wait else ""


@keyword
def closeApp(ad, pkgname):
    """
    停止app
    :param ad: 
    :param pkgname: 
    :return: 
    """
    ad.app_stop(pkgname)


@keyword
def touchById(ad, id):
    """
    根据id点击
    :param ad: 
    :param id: 
    :return: 
    """
    ad(resourceId=id).click()


@keyword
def sendText(ad, text, **kwargs):
    """
    点击输入框,输入文本
    :param ad: 
    :param text: 需输入的文本
    :param kwargs: 用于定位输入框的参数
    :return: 
    """
    ad(**kwargs).set_text(text)


@keyword
def press(ad, key):
    """
    按键
    :param ad: 
    :param key: 
    :return: 
    """
    ad.press(key)


@keyword
def screenshot(ad):
    image = ad.screenshot()
    image.save("home.jpg")
