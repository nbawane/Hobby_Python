# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class SentryHookTests(WebhookTestCase):
    STREAM_NAME = 'sentry'
    URL_TEMPLATE = "/api/v1/external/sentry?&api_key={api_key}"
    FIXTURE_DIR_NAME = 'sentry'

    def test_error_issue_message(self):
        # type: () -> None
        expected_subject = u"zulip"
        expected_message = u"New ERROR [issue](https://sentry.io/zulip/zulip/issues/156699934/): This is an example python exception."
        self.send_and_test_stream_message(
            'exception_message',
            expected_subject,
            expected_message
        )
