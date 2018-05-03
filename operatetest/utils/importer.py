import importlib
import os, sys
from ..utils.log import logger

def import_module(module_path):
    if not os.path.exists(module_path):
        raise Exception("module path not exists")

    dirname, filename = os.path.split(module_path)
    sys.path.insert(0, dirname)

    filename = filename[:-3]
    try:
        module = importlib.import_module(filename)
        return module
    except ImportError as e:
        logger.exception(e)
        raise Exception("module can not import")
