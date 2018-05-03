# coding: utf-8
# created by yang

__all__ = ["logger", "BASE_DIR", "config","TestCase"]

VERSION = "1.0.0"

from .conf.settings import BASE_DIR
from .auxiliary import VAR as config
from .utils.log import logger
from .core.testcase import TestCase


logger.info("-----------------------  Operate Test Version {}  -----------------------".format(VERSION))
