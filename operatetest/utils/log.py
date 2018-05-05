"""
from utils.log import logger
logger.info('test log')
"""
import sys

from operatetest.auxiliary import settings
from . import files
from . import logging
from ..auxiliary import VAR

__all__ = ["Logger","logger"]

class Logger(object):

    def __init__(self,logger,console_handler):
        self.logger = logger
        self.console_handler=console_handler

    def debug(self,msg):
        self.console_handler.stream = sys.stdout
        self.logger.debug(msg)
        self.console_handler.stream = sys.stderr

    def info(self,msg,iskeyword=False):
        self.console_handler.stream = sys.stdout
        if iskeyword:
            self.logger.info(msg,iskeyword=True)
        else:
            self.logger.info(msg)
        self.console_handler.stream = sys.stderr

    def warn(self,msg):
        self.console_handler.stream = sys.stdout
        self.logger.warn(msg)
        self.console_handler.stream = sys.stderr

    def error(self,msg):
        self.logger.error(msg)

    def fatal(self,msg):
        self.logger.fatal(msg)

    def exception(self, msg):
        self.logger.exception(msg)


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

        # cls.formatter = logging.Formatter('%(asctime)s  %(name)s %(levelname)s : %(message)s')
        cls.console_pattern = logging.Formatter(settings.LOG['console_pattern'])
        cls.file_pattern = logging.Formatter(settings.LOG['file_pattern'])

        if not cls.logger.handlers:  # 避免重复日志
            cls.console_handler = logging.StreamHandler()
            cls.console_handler.setFormatter(cls.console_pattern)
            cls.console_handler.setLevel(cls.console_output_level)
            cls.logger.addHandler(cls.console_handler)

            file_handler = logging.FileHandler(filename=files.path_join(VAR.report_dir, settings.LOG["file_name"]), encoding='utf-8')
            file_handler.setFormatter(cls.file_pattern)
            file_handler.setLevel(cls.file_output_level)
            cls.logger.addHandler(file_handler)
        return cls(cls.logger,cls.console_handler)

#
#
#
# class Logger(object):
#
#     @classmethod
#     def get_logger(cls,logger_name='operatetest'):
#         """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
#         我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
#         两个句柄的日志级别不同，在配置文件中可设置。
#         """
#         cls.logger = logging.getLogger(logger_name)
#         logging.root.setLevel(logging.NOTSET)
#
#         # level
#         cls.console_output_level = settings.LOG['console_level']
#         cls.file_output_level = settings.LOG['file_level']
#
#         cls.console_pattern = logging.Formatter(settings.LOG['console_pattern'])
#         cls.file_pattern = logging.Formatter(settings.LOG['file_pattern'])
#
#         if not cls.logger.handlers:  # 避免重复日志
#             console_handler = logging.StreamHandler()
#             console_handler.setFormatter(cls.console_pattern)
#             console_handler.setLevel(cls.console_output_level)
#             cls.logger.addHandler(console_handler)
#
#             file_handler = FileHandler(filename=path_join(VAR.report_dir,settings.LOG["file_name"]),encoding='utf-8')
#             file_handler.setFormatter(cls.file_pattern)
#             file_handler.setLevel(cls.file_output_level)
#             cls.logger.addHandler(file_handler)
#         return cls.logger

logger = Logger.get_logger()