import unittest

from .runner import HTMLTestRunner
from ..auxiliary import VAR
from .. import utils
from ..utils import importer
from ..utils.log import logger
from ..conf import settings
from .uiautomator import connect


def initialize():
    try:
        ad = connect(VAR.device_ip)
        # ad = connect()
        logger.debug("device info:{}".format(ad.info))
        setattr(VAR,"ad",ad)
    except Exception as e:
        raise Exception("连接手机失败,请检查手机IP是否配置正确!")



def run():
    # print("start run")
    # print(VAR.driver_dir)
    # print(VAR.report_dir)
    #
    # a = Driver.driver()
    # b = Driver.driver()
    #
    # print(type(a))
    # print(type(b))
    # print(a is b)
    #
    # a.close()

    # 1
    initialize()


    # 2、执行顺序是安加载顺序：先执行test_sub，再执行test_add
    tests = []
    loader = unittest.TestLoader()
    scripts_dir = utils.path_join(settings.BASE_DIR, "scripts", VAR.scripts_run)
    scripts = utils.get_all_files(scripts_dir)

    for script in scripts:
        print(script)
        module = importer.import_module(script)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                tests.append(loader.loadTestsFromTestCase(obj))

    # tests.append(loader.loadTestsFromModule(module))

    suite = unittest.TestSuite(tests)
    """
        suite = unittest.TestSuite()

    tests = [TestMathFunc("test_add"), TestMathFunc("test_minus"), TestMathFunc("test_divide")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    """

    report = VAR.report_dir + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='修改html报告')
        runner.run(suite)
