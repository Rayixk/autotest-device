# -*- coding:utf-8 -*-

"""
@Title：JOOM测试-商品搜索T-sheet测试
@Desc：pass
@Author：yang
@Date Created：2018-05-03
@Date Last Modified：2018-05-03
@Step：
"""

from aw import *
from operatetest import *


class Test_001(TestCase):
    def setUp(self):
        Common.launchApp(self.ad, 'com.joom')
        pass

    def test(self):
        Common.touchById(self.ad, "com.joom:id/menu_search")
        # Common.touchById(self.ad, "com.joom:id/search_field")
        # Common.sendText(self.ad, "T-sheet", resourceId="com.joom:id/query_field")
        # Common.press(self.ad, "enter")
        # Common.sleep(5)

    def tearDown(self):
        Common.closeApp(self.ad, 'com.joom')
        pass
