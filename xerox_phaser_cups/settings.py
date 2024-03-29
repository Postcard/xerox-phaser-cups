
import os


class ImproperlyConfigured(Exception):
    pass


def get_env_setting(setting, default=None):
    """ Get the environment setting or return exception """
    if setting in os.environ:
        return os.environ[setting]
    elif default is not None:
        return default
    else:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


PROJECT_PATH = '/usr/src/app/xerox_phaser_cups'

RESIN_UUID = get_env_setting('RESIN_DEVICE_UUID')

PRINTER_NAME = get_env_setting('PRINTER_NAME')

TOKEN = get_env_setting('TOKEN')

API_HOST = get_env_setting('API_HOST')

AWS_SQS_REGION = 'eu-west-1'

AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')

PHANTOMJS_PATH = '/usr/local/bin/phantomjs'

IMAGE_TO_PRINT = ("picture_color_1280", "picture_1280")[get_env_setting('COLOR_OR_BW') == "BW"]
