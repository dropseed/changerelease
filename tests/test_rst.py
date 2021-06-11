import os
from docutils.core import publish_string

def test_1():
    with open(os.path.join(os.path.dirname(__file__), "celery_changelog.rst"), "r") as f:
        rst = f.read()

    output = publish_string(source=rst, writer_name="html4css1").decode("utf-8")
    import ipdb; ipdb.set_trace()
