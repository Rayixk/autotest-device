"""
    report
"""
import re
import os
import copy
import datetime
from jinja2 import Template
from ..auxiliary import VAR, BASE_DIR


def generate_case_report(self):
    """self:instance of TestCase"""
    p = os.path.join(BASE_DIR, "operatetest", "resources", "template0.html")
    with open(p, encoding='utf-8') as f:
        content = f.read()

    template = Template(content)

    setup_msg, test_msg, teardown_msg = get_self_log(self)
    context = {
        "case": self,
        "setup_msg": setup_msg,
        "test_msg": test_msg,
        "teardown_msg": teardown_msg,
    }
    t = template.render(context)

    self.report_path = os.path.join(self.report_dir, "{}.html".format(self.case_name))
    with open(self.report_path, "w", encoding='utf-8') as f:
        f.write(t)
        f.flush()
    t = 'Generate TestCase Report > {}'.format(self.report_path)
    self.log.info(t)


def get_self_log(self):
    info = VAR.stdout.get_value()
    err = VAR.stderr.get_value()

    case_info = info[self.case_name] if self.case_name in info else []
    case_err = err[self.case_name] if self.case_name in err else []
    case_msg = [("info", *i) for i in case_info] + [("error", *i) for i in case_err]

    case_msg = bubble_sort(case_msg)  # 排序

    case_msg = [_x(i) for i in case_msg]  # 处理每个log的显示情况

    case_msg = x_(case_msg)  # 将error的前一个keyword标记为error

    return __x(case_msg)  # 截断log为三段


def x_(case_msg):
    """将error的前一个keyword,标记为error"""
    copy_case_msg = copy.deepcopy(case_msg)
    for i,j in enumerate(case_msg):
        if j[0] =="error" and not j[3]:
            k = _find(copy_case_msg,i)
            if k:
                copy_case_msg[k][0]="error"

    #如果setup end 是error的话,setup start 也标记为error,以此类推
    copy_case_msg = x__(copy_case_msg)
    return copy_case_msg

def x__(case_msg):
    """如果setup end 是error的话,setup start 也标记为error,以此类推"""
    d={
        "setUp_start":None,
        "setUp_end":None,  #<class 'tuple'>: (5, ['info', '2018-05-07 15:55:22.837', '------------------------------------ Test_001 setUp end  ---------------------------------------', 'setUp_end'])
        "test_start":None,
        "test_end":None,
        "tearDown_start":None,
        "tearDown_end":None,
    }

    for i,j in enumerate(case_msg):
        if j[3] in list(d.keys()):
            d[j[3]]=(i,j)

    if d['setUp_end'] and d['setUp_end'][1][0]=="error":
        case_msg[d["setUp_start"][0]][0]="error"

    if d['test_end'] and d['test_end'][1][0]=="error":
        case_msg[d["test_start"][0]][0]="error"

    if d['tearDown_end'] and d['tearDown_end'][1][0]=="error":
        case_msg[d["tearDown_start"][0]][0]="error"

    return case_msg



def _find(case_msg,index):
    copy_case_msg = copy.deepcopy(case_msg)
    for i in case_msg[index-1::-1]:
        if i[3]:
            return copy_case_msg.index(i)

def __x(case_msg):
    """截断log为三段"""
    copy_case_msg = copy.deepcopy(case_msg)
    setup_end_k = None
    test_end_k = None
    for i in case_msg:
        if i[3]:
            if "setUp_end" == i[3]:
                setup_end_k = copy_case_msg.index(i)
            elif "test_end" == i[3]:
                test_end_k = copy_case_msg.index(i)

    if not test_end_k:
        # 说明只执行了Setup,且发生了错误,test和teardown都没有执行
        return copy_case_msg, [], []

    return copy_case_msg[0:setup_end_k + 1], copy_case_msg[setup_end_k + 1:test_end_k + 1], copy_case_msg[
                                                                                            test_end_k + 1:]


def _x(i):
    """处理每个log的显示情况"""
    i = list(i)
    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', i[2]):
        a, b = i[2][23:].split(":", maxsplit=1)
        i[2] = b.strip()
    i[2] = i[2].strip("\n")
    if len(i) == 3:
        i.append("")

    return i


def gt(t1, t2):
    t1 = t1[1]
    t2 = t2[1]
    _t1, __t1 = t1.split(".")
    _t2, __t2 = t2.split(".")
    _t1 = datetime.datetime.strptime(_t1, "%Y-%m-%d %H:%M:%S")
    _t2 = datetime.datetime.strptime(_t2, "%Y-%m-%d %H:%M:%S")
    if _t1 == _t2:
        if int(__t1) == int(__t2):
            return False
        elif int(__t1) > int(__t2):
            return True
        elif int(__t1) < int(__t2):
            return False
    elif _t1 > _t2:
        return True
    elif _t1 < _t2:
        return False


def bubble_sort(li):
    for i in range(len(li) - 1):
        for j in range(len(li) - i - 1):
            if gt(li[j], li[j + 1]):
                li[j], li[j + 1] = li[j + 1], li[j]

    return li
