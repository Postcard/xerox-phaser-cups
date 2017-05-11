import time
import signal
import logging

import figure

from .workers import CUPSWorker
import settings

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

figure.api_base = settings.API_HOST
figure.token = settings.TOKEN


class GracefulKiller:

    kill_now = False

    def __init__(self, workers):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.workers = workers

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
        for worker in self.workers:
            worker.stop()

if __name__ == '__main__':

    logging.info("Starting CUPS worker")

    printer = figure.Printer.get(settings.RESIN_UUID)
    sqs_queue = printer.get('sqs_queue_name')

    cups_worker = CUPSWorker(sqs_queue)

    cups_worker.start()

    killer = GracefulKiller([cups_worker])

    while not killer.kill_now:
        time.sleep(5)