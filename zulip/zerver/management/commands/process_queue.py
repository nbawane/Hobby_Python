from __future__ import absolute_import

from types import FrameType
from typing import Any, List

from argparse import ArgumentParser
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.conf import settings
from django.utils import autoreload
from zerver.worker.queue_processors import get_worker, get_active_worker_queues
import sys
import signal
import logging
import threading

class Command(BaseCommand):
    def add_arguments(self, parser):
        # type: (ArgumentParser) -> None
        parser.add_argument('--queue_name', metavar='<queue name>', type=str,
                            help="queue to process")
        parser.add_argument('--worker_num', metavar='<worker number>', type=int, nargs='?', default=0,
                            help="worker label")
        parser.add_argument('--all', dest="all", action="store_true", default=False,
                            help="run all queues")
        parser.add_argument('--multi_threaded', nargs='+',
                            metavar='<list of queue name>',
                            type=str, required=False,
                            help="list of queue to process")

    help = "Runs a queue processing worker"

    def handle(self, *args, **options):
        # type: (*Any, **Any) -> None
        logging.basicConfig()
        logger = logging.getLogger('process_queue')

        if not settings.USING_RABBITMQ:
            # Make the warning silent when running the tests
            if settings.TEST_SUITE:
                logger.info("Not using RabbitMQ queue workers in the test suite.")
            else:
                logger.error("Cannot run a queue processor when USING_RABBITMQ is False!")
            sys.exit(1)

        def run_threaded_workers(queues, logger):
            # type: (List[str], logging.Logger) -> None
            cnt = 0
            for queue_name in queues:
                if not settings.DEVELOPMENT:
                    logger.info('launching queue worker thread ' + queue_name)
                cnt += 1
                td = Threaded_worker(queue_name)
                td.start()
            assert len(queues) == cnt
            logger.info('%d queue worker threads were launched' % (cnt,))

        if options['all']:
            autoreload.main(run_threaded_workers, (get_active_worker_queues(), logger))
        elif options['multi_threaded']:
            queues = options['multi_threaded']
            autoreload.main(run_threaded_workers, (queues, logger))
        else:
            queue_name = options['queue_name']
            worker_num = options['worker_num']

            logger.info("Worker %d connecting to queue %s" % (worker_num, queue_name))
            worker = get_worker(queue_name)
            worker.setup()

            def signal_handler(signal, frame):
                # type: (int, FrameType) -> None
                logger.info("Worker %d disconnecting from queue %s" % (worker_num, queue_name))
                worker.stop()
                sys.exit(0)
            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)

            worker.start()

class Threaded_worker(threading.Thread):
    def __init__(self, queue_name):
        # type: (str) -> None
        threading.Thread.__init__(self)
        self.worker = get_worker(queue_name)

    def run(self):
        # type: () -> None
        self.worker.setup()
        logging.debug('starting consuming ' + self.worker.queue_name)
        self.worker.start()
