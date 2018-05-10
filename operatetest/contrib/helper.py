import os
import unittest
from . import settings, VAR,logger
from .. import utils

__all__ = ["get_tests"]


def get_scripts():
    scripts = []
    for i in VAR.scripts_run.split(","):
        if not i:
            continue
        scripts_dir = os.path.join(settings.BASE_DIR, "scripts", i)
        if not os.path.exists(scripts_dir):
            raise Exception("{} 目标路径不存在,请检查配置文件scripts_run节点是否配置正确.".format(scripts_dir))
        scripts += utils.get_all_files(scripts_dir)

    return scripts


def get_tests():
    if VAR.mode != 1:
        logger.info("Execute in Debug Mode")

    tests = []

    scripts = []
    if VAR.mode == 1:
        scripts = get_scripts()
    elif VAR.mode == 2:
        with open(os.path.join(settings.BASE_DIR, "scripts", "scripts"), "r", encoding="utf-8") as f:
            scripts = [f.read(), ]
    elif VAR.mode == 3:
        scripts = [os.path.join(settings.BASE_DIR, "scripts", "Temp.py"), ]

    loader = unittest.TestLoader()

    for script in scripts:
        module = utils.import_module(script)
        file_name = os.path.basename(script)[:-3]

        obj = getattr(module, file_name, None)

        if not obj:
            raise Exception("在测试用例：{}中未获取到测试类：{}，测试类名需和测试用例名保持一致".format(script, file_name))

        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            tests.append(loader.loadTestsFromTestCase(obj))
        else:
            raise Exception("测试用例：{}中的测试类：{}不是TestCase的子类，请继承TestCase".format(script, file_name))

    return tests
