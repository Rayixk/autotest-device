import os,sys,time,unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from operatetest.auxiliary import VAR
from operatetest.auxiliary import settings
from operatetest.core import connect
from operatetest import utils

logger = utils.logger



def initialize():
    try:
        ad = connect(VAR.device_ip)
        setattr(ad, "click_post_delay", 0.5)
        # ad = connect()
        logger.debug("device info:{}".format(ad.info))
        setattr(VAR, "ad", ad)
    except Exception as e:
        raise Exception("连接手机失败,请检查手机IP是否配置正确!")


def get_scripts():
    scripts = []
    for i in VAR.scripts_run.split(","):
        if not i:
            continue
        scripts_dir = utils.path_join(settings.BASE_DIR, "scripts", i)
        if not os.path.exists(scripts_dir):
            raise Exception("{} 目标路径不存在,请检查配置文件scripts_run节点是否配置正确.".format(scripts_dir))
        scripts += utils.get_all_files(scripts_dir)

    return scripts


if __name__ == '__main__':

    # 1
    # initialize()

    # 2、执行顺序是安加载顺序：先执行test_sub，再执行test_add
    tests = []
    loader = unittest.TestLoader()

    scripts = get_scripts()

    for script in scripts:
        module = utils.import_module(script)
        for name in dir(module):
            if name in ["TestCase",]:
                continue
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                tests.append(loader.loadTestsFromTestCase(obj))


    suite = unittest.TestSuite(tests)

    from operatetest.core.runner import TextTestRunner

    runner = TextTestRunner(descriptions='task_{}'.format(VAR.project_start_time))
    result = runner.run(suite)

    from operatetest.core.report import generate_task_report

    result.log = logger
    generate_task_report(result)

    # print(VAR.stdout.get_value())
    # print(VAR.stderr.get_value())

