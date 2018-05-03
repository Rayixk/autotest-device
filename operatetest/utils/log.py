"""
from utils.log import logger
logger.info('test log')
"""

import logging
from logging import FileHandler
from ..conf import settings
from ..auxiliary import VAR
from ..utils import path_join

class Logger(object):
    def __init__(self,logger_name='operatetest'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)

        # level
        self.console_output_level = settings.LOG['console_level']
        self.file_output_level = settings.LOG['file_level']

        self.formatter = logging.Formatter(settings.LOG['pattern'])

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。
        """
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            file_handler = FileHandler(filename=path_join(VAR.report_dir,settings.LOG["file_name"]),encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()