"""
from utils.log import logger
logger.info('test log')
"""
import sys,os

from . import logging
from ..auxiliary import VAR,settings

__all__ = ["Logger","logger"]

class Logger(object):

    def __init__(self,logger,console_handler):
        self.logger = logger
        self.console_handler=console_handler

    def debug(self,msg,**kwargs):
        self.console_handler.stream = sys.stdout
        self.logger.debug(msg,**kwargs)
        self.console_handler.stream = sys.stderr

        if getattr(logging, "DEBUG") < getattr(logging, settings.LOG['console_level']):
            #说明debug的内容不会被输出到控制台,需要单独加入stdout
            if "img_path" in kwargs:
                VAR.stdout.l.append(msg, *list(kwargs.keys()))


    def info(self,msg,**kwargs):
        self.console_handler.stream = sys.stdout
        self.logger.info(msg, **kwargs)
        self.console_handler.stream = sys.stderr

    def warn(self,msg):
        self.console_handler.stream = sys.stdout
        self.logger.warn(msg)
        self.console_handler.stream = sys.stderr

    def error(self,msg,**kwargs):
        self.logger.error(msg,**kwargs)

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

            file_handler = logging.FileHandler(filename=os.path.join(VAR.report_dir, "task_{}.log".format(VAR.project_start_time)), encoding='utf-8')
            file_handler.setFormatter(cls.file_pattern)
            file_handler.setLevel(cls.file_output_level)
            cls.logger.addHandler(file_handler)
        return cls(cls.logger,cls.console_handler)

logger = Logger.get_logger()