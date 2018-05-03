import os

__all__ = ["path_join","make_dirs","get_all_files"]


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





if __name__ == '__main__':
    # print(path_join(r"D:\dev\workspace\aototest","drivers"))
    s = get_all_files(r"D:\dev\workspace\aototest\scripts")
    for i in s:
        print(i)