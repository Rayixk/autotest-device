import os, sys, unittest

_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _base_dir)

from operatetest import *

def initialize():
    try:
        try:
            if VAR.sn:
                from operatetest.core.adbutil import Adb
                if not Adb(VAR.sn).launch_and_check():
                    raise Exception("launch atx-agent daemon failure")
            ad = connect(VAR.sn)
        except Exception as e:
            ad = connect(VAR.device_ip)

        setattr(ad, "click_post_delay", 1)  # 设置每次点击后,等待1s
        logger.debug("device info:{}".format(ad.info))
        setattr(VAR, "ad", ad)

    except Exception as e:
        raise Exception("连接手机失败,请检查手机sn或ip是否配置正确!")


if __name__ == '__main__':

    tests = get_tests()

    initialize()

    suite = unittest.TestSuite(tests)

    from operatetest.core.runner import TextTestRunner

    runner = TextTestRunner(descriptions='task_{}'.format(VAR.project_start_time))
    result = runner.run(suite)

    from operatetest.core.report import generate_task_report

    result.log = logger
    generate_task_report(result)
