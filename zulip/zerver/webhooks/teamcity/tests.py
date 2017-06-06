# -*- coding: utf-8 -*-
import ujson
from zerver.models import Recipient
from zerver.lib.test_classes import WebhookTestCase

class TeamcityHookTests(WebhookTestCase):
    STREAM_NAME = 'teamcity'
    URL_TEMPLATE = u"/api/v1/external/teamcity?stream={stream}&api_key={api_key}"
    SUBJECT = u"Project :: Compile"
    FIXTURE_DIR_NAME = 'teamcity'

    def test_teamcity_success(self):
        # type: () -> None
        expected_message = u"Project :: Compile build 5535 - CL 123456 was successful! :thumbsup:\nDetails: [changes](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952&tab=buildChangesDiv), [build log](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952)"
        self.send_and_test_stream_message('success', self.SUBJECT, expected_message)

    def test_teamcity_broken(self):
        # type: () -> None
        expected_message = u"Project :: Compile build 5535 - CL 123456 is broken with status Exit code 1 (new)! :thumbsdown:\nDetails: [changes](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952&tab=buildChangesDiv), [build log](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952)"
        self.send_and_test_stream_message('broken', self.SUBJECT, expected_message)

    def test_teamcity_failure(self):
        # type: () -> None
        expected_message = u"Project :: Compile build 5535 - CL 123456 is still broken with status Exit code 1! :thumbsdown:\nDetails: [changes](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952&tab=buildChangesDiv), [build log](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952)"
        self.send_and_test_stream_message('failure', self.SUBJECT, expected_message)

    def test_teamcity_fixed(self):
        # type: () -> None
        expected_message = u"Project :: Compile build 5535 - CL 123456 has been fixed! :thumbsup:\nDetails: [changes](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952&tab=buildChangesDiv), [build log](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952)"
        self.send_and_test_stream_message('fixed', self.SUBJECT, expected_message)

    def test_teamcity_personal(self):
        # type: () -> None
        expected_message = u"Your personal build of Project :: Compile build 5535 - CL 123456 is broken with status Exit code 1 (new)! :thumbsdown:\nDetails: [changes](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952&tab=buildChangesDiv), [build log](http://teamcity/viewLog.html?buildTypeId=Project_Compile&buildId=19952)"
        payload = ujson.dumps(ujson.loads(self.fixture_data(self.FIXTURE_DIR_NAME, 'personal')))
        self.client_post(self.url, payload, content_type="application/json")
        msg = self.get_last_message()

        self.assertEqual(msg.content, expected_message)
        self.assertEqual(msg.recipient.type, Recipient.PERSONAL)
