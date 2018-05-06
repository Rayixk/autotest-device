"""
    report
"""
import os
from jinja2 import Template
from ..auxiliary import BASE_DIR


def generate_case_report(self):
    """self:instance of TestCase"""
    p = os.path.join(BASE_DIR,"operatetest","resources","case_report_template.html")
    with open(p,encoding='utf-8') as f:
        content = f.read()

    template = Template(content)

    context = {
        "case": self
    }
    t = template.render(context)

    self.report_path = os.path.join(self.report_dir,"{}.html".format(self.case_name))
    with open(self.report_path, "w", encoding='utf-8') as f:
        f.write(t)
        f.flush()
    t = 'generate case report > {}'.format(self.report_path)
    self.log.info(t)
