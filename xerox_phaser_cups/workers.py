import threading
import logging
import time
import json
import tempfile
import io
import os

import cups
import boto3

import settings
import phantomjs

from renderer import render
from utils import merge_pdf

logger = logging.getLogger(__name__)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)


class StoppableThreadMixin(object):

    def __init__(self, *args, **kwargs):
        super(StoppableThreadMixin, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class PrinterNotFoundException(Exception):
    pass


def get_sqs_resource():
    return boto3.resource(
        'sqs',
        settings.AWS_SQS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


class CUPSWorker(StoppableThreadMixin, threading.Thread):

    def __init__(self, queue_name, *args, **kwargs):
        super(CUPSWorker, self).__init__(*args, **kwargs)
        sqs_resource = get_sqs_resource()
        self.queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
        self.new_test_print()

    def new_test_print(self):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, 'imp_figure.jpg')
        # self._print(file_path, settings.PRINTER_NAME)
        self._print(file_path, "DP_DS620")

    # def test_print(self, printer_name):
    #     dirname = os.path.dirname(__file__)
    #     file_path = os.path.join(dirname, 'imp_figure.jpg')
    #     print(file_path)
    #     open(file_path,"r").close()
    #     print("closed")

    #     conn = cups.Connection()
    #     printers = conn.getPrinters()
    #     printer = printers.get(printer_name)
    #     if not printer:
    #         raise PrinterNotFoundException()
    #     conn.getPPD(printer_name)
    #     print("printing:")
    #     result = conn.printFile(printer_name, file_path, 'poster', {})
    #     if result == 0:
    #         print("error")
    #     else:
    #         print("job id:")
    #         print(result)
    #         jobs = conn.getJobs()
    #         print(jobs)

    def _print(self, file_path, printer_name):
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer = printers.get(printer_name)
        if not printer:
            raise PrinterNotFoundException()
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'B7'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w288h432'})
# #         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w288h432-div2'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w324h432'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w360h360'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w360h504'})
# #         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w360h504-div2'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w360h504-w360h360_w360h144'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h432'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h576'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h576-w432h432_w432h144'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h576-div4'})
# #         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h576-div2'})
#         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h648'})
# #         conn.printFile(printer_name, file_path, 'poster', {'PageSize': 'w432h648-div2'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'B7'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w288h432'})
#         conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w288h432-div2'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w324h432'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w360h360'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w360h504'})
#         conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w360h504-div2'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w360h504-w360h360_w360h144'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h432'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h576'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h576-w432h432_w432h144'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h576-div4'})
#         conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h576-div2'})
        conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h648'})
#         conn.printFile(printer_name, file_path, 'poster', {'MediaSize': 'w432h648-div2'})
        print(conn.getJobs())

    def handle_print_job(self, print_job):
        portrait = print_job['portrait']
        picture_url = portrait['picture_1280']
        code = portrait['code']
        place = portrait.get('place')
        place_name = place['name'] if place else None
        event = portrait.get('event')
        event_name = event['name'] if event else None
        taken_str = portrait['taken_str']
        context = {
            'picture_url': picture_url,
            'code': code,
            'place_name': place_name,
            'event_name': event_name,
            'taken_str': taken_str,
            'css_url': 'file://%s/css/index.css' % settings.PROJECT_PATH
        }
        html = render(context)
        recto = phantomjs.get_screenshot(html)
        verso_path = '%s/resources/verso.pdf' % settings.PROJECT_PATH
        with open(verso_path) as verso_file:
            verso = verso_file.read()
        with tempfile.NamedTemporaryFile() as f:
            merge_pdf(verso, recto, f.name)
            print(f.name)
            self._print(f.name, settings.PRINTER_NAME)
            self._print(f.name, "DP_DS620")

    def run(self):
        while True:
            if self.stopped():
                logger.info("Bye Bye from cups worker")
                break
            else:
                try:
                    for message in self.queue.receive_messages(MaxNumberOfMessages=10):
                        print("PRINTING")
                        print_job = json.loads(message.body)
                        self.handle_print_job(print_job)
                        message.delete()
                except Exception as e:
                    logger.exception(e.message)
            time.sleep(0.5)