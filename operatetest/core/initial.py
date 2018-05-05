import sys
import time
from ..auxiliary.variable import VAR
from ..utils import logger

class TimeList(object):
    def __init__(self):
        self.l = []

    def append(self,*args):
        if len(args)==1 and args[0] =="\n":
            return
        self.l.append((self.now,*args))

    @property
    def now(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp
        self.l = TimeList()

    def write(self, s,**kwargs):
        self.fp.write(s)
        self.l.append(s,"iskeyword") if "iskeyword" in kwargs else self.l.append(s)


    def flush(self):
        self.fp.flush()

    def get_value(self):
        return self.l.l


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)
sys.stdout = stdout_redirector
sys.stderr = stderr_redirector




























