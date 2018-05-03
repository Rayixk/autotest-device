from aw import *
from operatetest import *


class Test_001(TestCase):
    def setUp(self):
        pass

    def test(self):
        common.launchApp(self.ad,'com.netease.cloudmusic')
        common.touchByText(self.ad,'私人FM')
        common.touchByDesc(self.ad,'转到上一层级')

        common.touchByText(self.ad, '每日推荐')
        common.touchByDesc(self.ad, '转到上一层级')

        common.touchByText(self.ad, '歌单')
        common.touchByDesc(self.ad, '转到上一层级')

        common.touchByText(self.ad, '排行榜')
        common.touchByDesc(self.ad, '转到上一层级')

        common.stopApp(self.ad, 'com.netease.cloudmusic')

    def tearDown(self):
        pass
