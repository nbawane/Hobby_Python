# Webhooks for external integrations.
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from zerver.lib.actions import check_send_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile
from django.http import HttpRequest, HttpResponse
from typing import Any, Dict, Text

CRASHLYTICS_SUBJECT_TEMPLATE = '{display_id}: {title}'
CRASHLYTICS_MESSAGE_TEMPLATE = '[Issue]({url}) impacts at least {impacted_devices_count} device(s).'

CRASHLYTICS_SETUP_SUBJECT_TEMPLATE = "Setup"
CRASHLYTICS_SETUP_MESSAGE_TEMPLATE = "Webhook has been successfully configured."

VERIFICATION_EVENT = 'verification'


@api_key_only_webhook_view('Crashlytics')
@has_request_variables
def api_crashlytics_webhook(request, user_profile, payload=REQ(argument_type='body'),
                            stream=REQ(default='crashlytics')):
    # type: (HttpRequest, UserProfile, Dict[str, Any], Text) -> HttpResponse
    try:
        event = payload['event']
        if event == VERIFICATION_EVENT:
            subject = CRASHLYTICS_SETUP_SUBJECT_TEMPLATE
            body = CRASHLYTICS_SETUP_MESSAGE_TEMPLATE
        else:
            issue_body = payload['payload']
            subject = CRASHLYTICS_SUBJECT_TEMPLATE.format(
                display_id=issue_body['display_id'],
                title=issue_body['title']
            )
            body = CRASHLYTICS_MESSAGE_TEMPLATE.format(
                impacted_devices_count=issue_body['impacted_devices_count'],
                url=issue_body['url']
            )
    except KeyError as e:
        return json_error(_("Missing key {} in JSON".format(str(e))))

    check_send_message(user_profile, request.client, 'stream', [stream],
                       subject, body)
    return json_success()
