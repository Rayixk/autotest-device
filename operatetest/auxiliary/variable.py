"""
Some auxiliary functions
"""
import datetime
import json
import os
import sys
import time

from . import settings
from .exception import ConfigNotExistError, ConfigParseError


def _config():
    config_path = os.path.join(settings.BASE_DIR, "project.config")
    if not os.path.exists(config_path):
        raise ConfigNotExistError("config not exist")

    with open(config_path, encoding="utf-8") as f:
        c = f.read()
    try:
        c = json.loads(c)
        return c
    except Exception as e:
        raise ConfigParseError(e)


class Variable(dict):
    def __init__(self, *args, **kwargs):
        super(Variable, self).__init__(*args, **kwargs)
        if "config" in kwargs:
            self.config = kwargs["config"]
        else:
            self.config = _config()

    def __getattr__(self, name):
        if not name in self.config:
            if name in ["cur_case_name", ]:
                return
            else:
                raise Exception('config has no attr "{}"'.format(name))
        value = self.config[name]
        if isinstance(value, dict):
            value = Variable(config=value)
        return value


VAR = Variable()


def handle_config():
    VAR.project_start_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    if not os.path.isabs(VAR.report_dir):
        VAR.report_dir = os.path.join(settings.BASE_DIR, VAR.report_dir, "task_{}".format(VAR.project_start_time))
    else:
        VAR.report_dir = os.path.join(VAR.report_dir, "task_{}".format(VAR.project_start_time))
    os.makedirs(VAR.report_dir, exist_ok=True)


class TimeList(object):
    def __init__(self):
        self.d = {}

    def append(self, *args):
        if len(args) == 1 and args[0] == "\n":
            return
        if VAR.cur_case_name:
            cur_case_name = VAR.cur_case_name
        else:
            cur_case_name = "operatetest"

        if cur_case_name in self.d:
            self.d[cur_case_name].append((self.now, *args))
        else:
            self.d[cur_case_name] = [(self.now, *args), ]

    @property
    def now(self):
        # ct = time.time()
        # local_time = time.localtime(ct)
        # data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        # data_secs = (ct - int(ct)) * 1000
        # time_stamp = "%s.%03d" % (data_head, data_secs)
        return str(datetime.datetime.now())[:-3]


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp
        self.l = TimeList()

    def write(self, s, **kwargs):
        self.fp.write(s)
        self.l.append(s, *list(kwargs.keys()))

    def flush(self):
        self.fp.flush()

    def get_value(self):
        return self.l.d


handle_config()

VAR.stdout = sys.stdout = OutputRedirector(sys.stdout)
VAR.stderr = sys.stderr = OutputRedirector(sys.stderr)
