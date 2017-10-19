import subprocess
import tempfile
from os.path import abspath, dirname, join

from . import settings


def get_screenshot(html):
    script_dir = abspath(dirname(__file__))
    with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
        script_path = join(script_dir, 'phantom.js')
        args = [settings.PHANTOMJS_PATH, script_path, html, f.name]
        subprocess.check_output(args)
        content = f.read()
    return content

