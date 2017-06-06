from __future__ import absolute_import
from __future__ import print_function

from django.core.management.base import BaseCommand
from django.utils.timezone import now as timezone_now
from typing import Any, Dict, List

from zerver.models import UserPresence, UserActivity
from zerver.lib.utils import statsd, statsd_key

from datetime import datetime, timedelta
from collections import defaultdict

class Command(BaseCommand):
    help = """Sends active user statistics to statsd.

    Run as a cron job that runs every 10 minutes."""

    def handle(self, *args, **options):
        # type: (*Any, **Any) -> None
        # Get list of all active users in the last 1 week
        cutoff = timezone_now() - timedelta(minutes=30, hours=168)

        users = UserPresence.objects.select_related().filter(timestamp__gt=cutoff)

        # Calculate 10min, 2hrs, 12hrs, 1day, 2 business days (TODO business days), 1 week bucket of stats
        hour_buckets = [0.16, 2, 12, 24, 48, 168]
        user_info = defaultdict(dict)  # type: Dict[str, Dict[float, List[str]]]

        for last_presence in users:
            if last_presence.status == UserPresence.IDLE:
                known_active = last_presence.timestamp - timedelta(minutes=30)
            else:
                known_active = last_presence.timestamp

            for bucket in hour_buckets:
                if bucket not in user_info[last_presence.user_profile.realm.string_id]:
                    user_info[last_presence.user_profile.realm.string_id][bucket] = []
                if timezone_now() - known_active < timedelta(hours=bucket):
                    user_info[last_presence.user_profile.realm.string_id][bucket].append(last_presence.user_profile.email)

        for realm, buckets in user_info.items():
            print("Realm %s" % (realm,))
            for hr, users in sorted(buckets.items()):
                print("\tUsers for %s: %s" % (hr, len(users)))
                statsd.gauge("users.active.%s.%shr" % (statsd_key(realm, True), statsd_key(hr, True)), len(users))

        # Also do stats for how many users have been reading the app.
        users_reading = UserActivity.objects.select_related().filter(query="/json/messages/flags")
        user_info = defaultdict(dict)
        for activity in users_reading:
            for bucket in hour_buckets:
                if bucket not in user_info[activity.user_profile.realm.string_id]:
                    user_info[activity.user_profile.realm.string_id][bucket] = []
                if timezone_now() - activity.last_visit < timedelta(hours=bucket):
                    user_info[activity.user_profile.realm.string_id][bucket].append(activity.user_profile.email)
        for realm, buckets in user_info.items():
            print("Realm %s" % (realm,))
            for hr, users in sorted(buckets.items()):
                print("\tUsers reading for %s: %s" % (hr, len(users)))
                statsd.gauge("users.reading.%s.%shr" % (statsd_key(realm, True), statsd_key(hr, True)), len(users))
