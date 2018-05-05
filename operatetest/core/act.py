import os,sys,time,unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TimeList(object):
    def __init__(self):
        self.l = []

    def append(self, *args):
        if len(args) == 1 and args[0] == "\n":
            return
        self.l.append((self.now, *args))

    @property
    def now(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp
        self.l = TimeList()

    def write(self, s, **kwargs):
        self.fp.write(s)
        self.l.append(s, "iskeyword") if "iskeyword" in kwargs else self.l.append(s)

    def flush(self):
        self.fp.flush()

    def get_value(self):
        return self.l.l


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)
sys.stdout = stdout_redirector
sys.stderr = stderr_redirector

from operatetest.auxiliary import VAR
from operatetest.auxiliary import settings
from operatetest.core import connect
from operatetest import utils

logger = utils.logger
VAR.stdout = stdout_redirector
VAR.stderr = stderr_redirector


def initialize():
    try:
        ad = connect(VAR.device_ip)
        setattr(ad, "click_post_delay", 0.5)
        # ad = connect()
        logger.debug("device info:{}".format(ad.info))
        setattr(VAR, "ad", ad)
    except Exception as e:
        raise Exception("连接手机失败,请检查手机IP是否配置正确!")


if __name__ == '__main__':

    # 1
    initialize()

    # 2、执行顺序是安加载顺序：先执行test_sub，再执行test_add
    tests = []
    loader = unittest.TestLoader()
    scripts_dir = utils.path_join(settings.BASE_DIR, "scripts", VAR.scripts_run)
    scripts = utils.get_all_files(scripts_dir)

    for script in scripts:
        logger.info(script)
        module = utils.import_module(script)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                tests.append(loader.loadTestsFromTestCase(obj))


    suite = unittest.TestSuite(tests)

    report = VAR.report_dir + '\\report.html'
    # with open(report, 'wb') as f:
    #     runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='修改html报告')
    #     runner.run(suite)
    from unittest.runner import TextTestRunner

    runner = TextTestRunner()
    runner.run(suite)

    print(VAR.stdout.get_value())
    print(VAR.stderr.get_value())

