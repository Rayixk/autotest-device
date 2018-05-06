import importlib
import os, sys
from .log import logger

__all__ = ["path_join","make_dirs","get_all_files","import_module"]


def path_join(*args):
    return os.path.join(*args)


def make_dirs(path):
    os.makedirs(path,exist_ok=True)

def get_all_files(dirname):
    """返回dir文件夹下的所有的文件的路径"""
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if "__" in apath or ".pyc" in apath:
                continue
            result.append(apath)
    return result


def import_module(module_path):
    if not os.path.exists(module_path):
        raise Exception("module path not exists")

    dirname, filename = os.path.split(module_path)
    sys.path.insert(0, dirname)

    filename = filename[:-3]
    try:
        module = importlib.import_module(filename)
        sys.path.pop(0)
        return module
    except ImportError as e:
        logger.exception(e)
        raise Exception("module can not import")



if __name__ == '__main__':
    # print(path_join(r"D:\dev\workspace\aototest","drivers"))
    s = get_all_files(r"D:\dev\workspace\aototest\scripts")
    for i in s:
        print(i)
