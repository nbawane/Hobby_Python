from __future__ import absolute_import

from typing import Any

from argparse import ArgumentParser
from django.core.management.base import BaseCommand
from zerver.lib.cache_helpers import fill_remote_cache, cache_fillers

class Command(BaseCommand):
    def add_arguments(self, parser):
        # type: (ArgumentParser) -> None
        parser.add_argument('--cache', dest="cache", default=None,
                            help="Populate the memcached cache of messages.")

    def handle(self, *args, **options):
        # type: (*Any, **str) -> None
        if options["cache"] is not None:
            fill_remote_cache(options["cache"])
            return

        for cache in cache_fillers.keys():
            fill_remote_cache(cache)
