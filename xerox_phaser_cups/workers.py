import threading
import logging
import time
import json
import tempfile
from urllib2 import urlopen

import cups
import boto3

import settings

logger = logging.getLogger(__name__)


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

    def __init__(self, queue_name):
        sqs_resource = get_sqs_resource()
        self.queue = sqs_resource.get_queue_by_name(queue_name)

    def _print(self, url):
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer = printers.get(settings.PRINTER_NAME)
        if not printer:
            raise PrinterNotFoundException()
        response = urlopen(url)
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(response.read())
            temp.flush()
            conn.printFile(XEROX_7100N, temp.name, 'poster')

    def handle_print_job(self, print_job):
        pdf_url = print_job.get('pdf_file')
        self._print(pdf_url)

    def run(self):
        while True:
            if self.stopped():
                logger.info("Bye Bye from cups worker")
                break
            else:
                try:
                    for message in self.queue.receive_messages(MaxNumberOfMessages=10):
                        print_job = json.loads(message.body)
                        self.handle_print_job(print_job)
                except Exception as e:
                    logger.exception(e.message)
            time.sleep(0.5)