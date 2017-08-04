from __future__ import absolute_import
from __future__ import print_function

from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from django.conf import settings

from zerver.models import Realm, Stream, UserProfile, Recipient, Subscription, \
    Message, UserMessage, Huddle, DefaultStream, RealmDomain, RealmFilter, Client
from zerver.lib.export import do_import_realm

import os
import subprocess
import sys
import ujson

from typing import Any
Model = Any  # TODO: make this mypy type more specific

class Command(BaseCommand):
    help = """Import Zulip database dump files into a fresh Zulip instance.

This command should be used only on a newly created, empty Zulip instance to
import a database dump from one or more JSON files.

Usage: ./manage.py import [--destroy-rebuild-database] [--import-into-nonempty] <export path name> [<export path name>...]"""

    def add_arguments(self, parser):
        # type: (CommandParser) -> None
        parser.add_argument('--destroy-rebuild-database',
                            dest='destroy_rebuild_database',
                            default=False,
                            action="store_true",
                            help='Destroys and rebuilds the databases prior to import.')

        parser.add_argument('--import-into-nonempty',
                            dest='import_into_nonempty',
                            default=False,
                            action="store_true",
                            help='Import into an existing nonempty database.')

    def new_instance_check(self, model):
        # type: (Model) -> None
        count = model.objects.count()
        if count:
            print("Zulip instance is not empty, found %d rows in %s table. "
                  % (count, model._meta.db_table))
            print("You may use --destroy-rebuild-database to destroy and rebuild the database prior to import.")
            exit(1)

    def do_destroy_and_rebuild_database(self, db_name):
        # type: (str) -> None
        call_command('flush', verbosity=0, interactive=False)
        subprocess.check_call([os.path.join(settings.DEPLOY_ROOT, "scripts/setup/flush-memcached")])

    def handle(self, *args, **options):
        # type: (*Any, **Any) -> None
        models_to_import = [Realm, Stream, UserProfile, Recipient, Subscription,
                            Client, Message, UserMessage, Huddle, DefaultStream, RealmDomain,
                            RealmFilter]

        if len(args) == 0:
            print("Please provide at least one realm dump to import.")
            exit(1)

        if options["destroy_rebuild_database"]:
            print("Rebuilding the database!")
            db_name = settings.DATABASES['default']['NAME']
            self.do_destroy_and_rebuild_database(db_name)
        elif not options["import_into_nonempty"]:
            for model in models_to_import:
                self.new_instance_check(model)

        for path in args:
            if not os.path.exists(path):
                print("Directory not found: '%s'" % (path,))
                exit(1)

            print("Processing dump: %s ..." % (path,))
            do_import_realm(path)
