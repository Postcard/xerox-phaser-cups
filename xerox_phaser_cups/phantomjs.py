import subprocess
from os.path import abspath, dirname, join

from . import settings


def get_screenshot(html, file_path):
    script_dir = abspath(dirname(__file__))
    script_path = join(script_dir, 'phantom.js')
    args = [settings.PHANTOMJS_PATH, script_path, html, file_path]
    subprocess.call(args)

