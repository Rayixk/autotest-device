# coding: utf-8
# created by yang

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



LOG = {
    "console_level": "INFO",
    "file_level": "DEBUG",
    "console_pattern": "%(asctime)s  %(levelname)s : %(message)s",
    "file_pattern": "%(asctime)s  %(name)s  %(levelname)s : %(message)s",
}



CONTENT = """
from aw import *
from operatetest import *


class Temp(TestCase):
    def setUp(self):
        pass

    def test(self):
{{ content }}

    def tearDown(self):
        pass


"""
