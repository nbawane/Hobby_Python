# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class ZapierHookTests(WebhookTestCase):
    STREAM_NAME = 'zapier'
    URL_TEMPLATE = "/api/v1/external/zapier?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'zapier'

    def test_zapier_when_subject_and_body_are_correct(self):
        # type: () -> None
        expected_subject = u"New email from zulip@zulip.com"
        expected_message = u"Your email content is: \nMy Email content."
        self.send_and_test_stream_message('correct_subject_and_body', expected_subject, expected_message)
