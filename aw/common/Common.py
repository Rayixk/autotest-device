import time


def sleep(n):
    time.sleep(n)


def touchByText(ad, text):
    """
    根据文本点击
    :param ad: 
    :param text: 
    :return: 
    """
    ad(text=text).click()


def touchByDesc(ad, desc):
    """
    根据描述点击
    :param ad: 
    :param desc: 
    :return: 
    """
    ad(description=desc).click()


def launchApp(ad, pkgname):
    """
    启动app
    :param ad: 
    :param pkgname: 
    :return: 
    """
    ad.app_start(pkgname)


def closeApp(ad, pkgname):
    """
    停止app
    :param ad: 
    :param pkgname: 
    :return: 
    """
    ad.app_stop(pkgname)


def touchById(ad, id):
    """
    根据id点击
    :param ad: 
    :param id: 
    :return: 
    """
    ad(resourceId=id).click()


def sendText(ad, text, **kwargs):
    """
    点击输入框,输入文本
    :param ad: 
    :param text: 需输入的文本
    :param kwargs: 用于定位输入框的参数
    :return: 
    """
    ad(**kwargs).set_text(text)

def press(ad,key):
    """
    按键
    :param ad: 
    :param key: 
    :return: 
    """
    ad.press(key)
