from __future__ import absolute_import
from django.http import HttpRequest, HttpResponse

from zerver.decorator import REQ
from zerver.models import UserProfile
from zerver.lib.validator import check_int
from zerver.lib.response import json_success
from zerver.lib.attachments import user_attachments, remove_attachment, \
    access_attachment_by_id


def list_by_user(request, user_profile):
    # type: (HttpRequest, UserProfile) -> HttpResponse
    return json_success({"attachments": user_attachments(user_profile)})


def remove(request, user_profile, attachment_id=REQ(validator=check_int)):
    # type: (HttpRequest, UserProfile, int) -> HttpResponse
    attachment = access_attachment_by_id(user_profile, attachment_id,
                                         needs_owner=True)
    remove_attachment(user_profile, attachment)
    return json_success()
