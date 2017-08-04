from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
settings.RUNNING_INSIDE_TORNADO = True
# We must call zerver.tornado.ioloop_logging.instrument_tornado_ioloop
# before we import anything else from our project in order for our
# Tornado load logging to work; otherwise we might accidentally import
# zerver.lib.queue (which will instantiate the Tornado ioloop) before
# this.
from zerver.tornado.ioloop_logging import instrument_tornado_ioloop
instrument_tornado_ioloop()

from django.core.management.base import BaseCommand, CommandError, CommandParser
from tornado import ioloop
from tornado.log import app_log
from typing import Callable

from zerver.lib.debug import interactive_debug_listen
from zerver.lib.queue import setup_tornado_rabbitmq
from zerver.tornado.application import create_tornado_application
from zerver.tornado.event_queue import add_client_gc_hook, \
    missedmessage_hook, process_notification, setup_event_queue
from zerver.tornado.socket import respond_send_message

import logging
import sys

if settings.USING_RABBITMQ:
    from zerver.lib.queue import get_queue_client


def handle_callback_exception(callback):
    # type: (Callable) -> None
    logging.exception("Exception in callback")
    app_log.error("Exception in callback %r", callback, exc_info=True)

class Command(BaseCommand):
    help = "Starts a Tornado Web server wrapping Django."

    def add_arguments(self, parser):
        # type: (CommandParser) -> None
        parser.add_argument('addrport', nargs="?", type=str,
                            help='[optional port number or ipaddr:port]\n '
                                 '(use multiple ports to start multiple servers)')

        parser.add_argument('--nokeepalive', action='store_true',
                            dest='no_keep_alive', default=False,
                            help="Tells Tornado to NOT keep alive http connections.")

        parser.add_argument('--noxheaders', action='store_false',
                            dest='xheaders', default=True,
                            help="Tells Tornado to NOT override remote IP with X-Real-IP.")

    def handle(self, addrport, **options):
        # type: (str, **bool) -> None
        interactive_debug_listen()

        import django
        from tornado import httpserver

        try:
            addr, port = addrport.split(':')
        except ValueError:
            addr, port = '', addrport

        if not addr:
            addr = '127.0.0.1'

        if not port.isdigit():
            raise CommandError("%r is not a valid port number." % (port,))

        xheaders = options.get('xheaders', True)
        no_keep_alive = options.get('no_keep_alive', False)
        quit_command = 'CTRL-C'

        if settings.DEBUG:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(levelname)-8s %(message)s')

        def inner_run():
            # type: () -> None
            from django.conf import settings
            from django.utils import translation
            translation.activate(settings.LANGUAGE_CODE)

            print("Validating Django models.py...")
            self.check(display_num_errors=True)
            print("\nDjango version %s" % (django.get_version()))
            print("Tornado server is running at http://%s:%s/" % (addr, port))
            print("Quit the server with %s." % (quit_command,))

            if settings.USING_RABBITMQ:
                queue_client = get_queue_client()
                # Process notifications received via RabbitMQ
                queue_client.register_json_consumer('notify_tornado', process_notification)
                queue_client.register_json_consumer('tornado_return', respond_send_message)

            try:
                # Application is an instance of Django's standard wsgi handler.
                application = create_tornado_application()

                # start tornado web server in single-threaded mode
                http_server = httpserver.HTTPServer(application,
                                                    xheaders=xheaders,
                                                    no_keep_alive=no_keep_alive)
                http_server.listen(int(port), address=addr)

                setup_event_queue()
                add_client_gc_hook(missedmessage_hook)
                setup_tornado_rabbitmq()

                instance = ioloop.IOLoop.instance()

                if django.conf.settings.DEBUG:
                    instance.set_blocking_log_threshold(5)
                    instance.handle_callback_exception = handle_callback_exception
                instance.start()
            except KeyboardInterrupt:
                sys.exit(0)

        inner_run()
