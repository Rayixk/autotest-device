# coding: utf-8
# created by yang

import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



LOG = {
    "file_name": "task.log",
    "console_level": "INFO",
    "file_level": "DEBUG",
    "pattern": "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
}
