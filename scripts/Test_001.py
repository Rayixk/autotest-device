from aw import *
from operatetest import *


class Test_001(TestCase):
    def setUp(self):
        pass

    def test(self):
        Common.launchApp(self.ad,'com.netease.cloudmusic')
        Common.touchByText(self.ad,'私人FM')
        Common.touchByDesc(self.ad,'转到上一层级')

        Common.touchByText(self.ad, '每日推荐')
        Common.touchByDesc(self.ad, '转到上一层级')

        Common.touchByText(self.ad, '歌单')
        Common.touchByDesc(self.ad, '转到上一层级')

        Common.touchByText(self.ad, '排行榜')
        Common.touchByDesc(self.ad, '转到上一层级')

        # Common.stopApp(self.ad, 'com.netease.cloudmusic')
    def tearDown(self):
        pass
