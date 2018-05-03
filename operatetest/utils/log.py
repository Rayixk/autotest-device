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

    @classmethod
    def get_logger(cls,logger_name='operatetest'):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。
        """
        cls.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)

        # level
        cls.console_output_level = settings.LOG['console_level']
        cls.file_output_level = settings.LOG['file_level']

        cls.formatter = logging.Formatter(settings.LOG['pattern'])

        if not cls.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(cls.formatter)
            console_handler.setLevel(cls.console_output_level)
            cls.logger.addHandler(console_handler)

            file_handler = FileHandler(filename=path_join(VAR.report_dir,settings.LOG["file_name"]),encoding='utf-8')
            file_handler.setFormatter(cls.formatter)
            file_handler.setLevel(cls.file_output_level)
            cls.logger.addHandler(file_handler)
        return cls.logger

logger = Logger.get_logger()