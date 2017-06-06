# -*- coding: utf-8 -*-
from __future__ import absolute_import
import types
from datetime import datetime, timedelta

from django.utils.timezone import now as timezone_now
from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.upload import create_attachment
from zerver.models import Message, Realm, Recipient, UserProfile, UserMessage, ArchivedUserMessage, \
    ArchivedMessage, Attachment, ArchivedAttachment
from zerver.lib.retention import get_expired_messages, move_message_to_archive

from typing import Any, List

from six.moves import range


class TestRetentionLib(ZulipTestCase):
    """
        Test receiving expired messages retention tool.
    """

    def setUp(self):
        # type: () -> None
        super(TestRetentionLib, self).setUp()
        self.zulip_realm = self._set_realm_message_retention_value('zulip', 30)
        self.mit_realm = self._set_realm_message_retention_value('zephyr', 100)

    @staticmethod
    def _set_realm_message_retention_value(realm_str, retention_period):
        # type: (str, int) -> Realm
        realm = Realm.objects.get(string_id=realm_str)
        realm.message_retention_days = retention_period
        realm.save()
        return realm

    @staticmethod
    def _change_messages_pub_date(msgs_ids, pub_date):
        # type: (List[int], datetime) -> Any
        messages = Message.objects.filter(id__in=msgs_ids).order_by('id')
        messages.update(pub_date=pub_date)
        return messages

    def _make_mit_messages(self, message_quantity, pub_date):
        # type: (int, datetime) -> Any
        # send messages from mit.edu realm and change messages pub date
        sender = self.mit_user('espuser')
        recipient = self.mit_user('starnine')
        msgs_ids = [self.send_message(sender.email, recipient.email, Recipient.PERSONAL) for i in
                    range(message_quantity)]
        mit_messages = self._change_messages_pub_date(msgs_ids, pub_date)
        return mit_messages

    def test_expired_messages_result_type(self):
        # type: () -> None
        # Check return type of get_expired_message method.
        result = get_expired_messages()
        self.assertIsInstance(result, types.GeneratorType)

    def test_no_expired_messages(self):
        # type: () -> None
        result = list(get_expired_messages())
        self.assertFalse(result)

    def test_expired_messages_in_each_realm(self):
        # type: () -> None
        # Check result realm messages order and result content
        # when all realm has expired messages.
        expired_mit_messages = self._make_mit_messages(3, timezone_now() - timedelta(days=101))
        self._make_mit_messages(4, timezone_now() - timedelta(days=50))
        zulip_messages_ids = Message.objects.order_by('id').filter(
            sender__realm=self.zulip_realm).values_list('id', flat=True)[3:10]
        expired_zulip_messages = self._change_messages_pub_date(zulip_messages_ids,
                                                                timezone_now() - timedelta(days=31))
        # Iterate by result
        expired_messages_result = [messages_list for messages_list in get_expired_messages()]
        self.assertEqual(len(expired_messages_result), 2)
        # Check mit.edu realm expired messages.
        self.assertEqual(len(expired_messages_result[0]['expired_messages']), 3)
        self.assertEqual(expired_messages_result[0]['realm_id'], self.mit_realm.id)
        # Check zulip.com realm expired messages.
        self.assertEqual(len(expired_messages_result[1]['expired_messages']), 7)
        self.assertEqual(expired_messages_result[1]['realm_id'], self.zulip_realm.id)
        # Compare expected messages ids with result messages ids.
        self.assertEqual(
            sorted([message.id for message in expired_mit_messages]),
            [message.id for message in expired_messages_result[0]['expired_messages']]
        )
        self.assertEqual(
            sorted([message.id for message in expired_zulip_messages]),
            [message.id for message in expired_messages_result[1]['expired_messages']]
        )

    def test_expired_messages_in_one_realm(self):
        # type: () -> None
        # Check realm with expired messages and messages
        # with one day to expiration data.
        expired_mit_messages = self._make_mit_messages(5, timezone_now() - timedelta(days=101))
        actual_mit_messages = self._make_mit_messages(3, timezone_now() - timedelta(days=99))
        expired_messages_result = list(get_expired_messages())
        expired_mit_messages_ids = [message.id for message in expired_mit_messages]
        expired_mit_messages_result_ids = [message.id for message in
                                           expired_messages_result[0]['expired_messages']]
        actual_mit_messages_ids = [message.id for message in actual_mit_messages]
        self.assertEqual(len(expired_messages_result), 1)
        self.assertEqual(len(expired_messages_result[0]['expired_messages']), 5)
        self.assertEqual(expired_messages_result[0]['realm_id'], self.mit_realm.id)
        # Compare expected messages ids with result messages ids.
        self.assertEqual(
            sorted(expired_mit_messages_ids),
            expired_mit_messages_result_ids
        )
        # Check actual mit.edu messages are not contained in expired messages list
        self.assertEqual(
            set(actual_mit_messages_ids) - set(expired_mit_messages_ids),
            set(actual_mit_messages_ids)
        )


class TestMoveMessageToArchive(ZulipTestCase):

    def setUp(self):
        # type: () -> None
        super(TestMoveMessageToArchive, self).setUp()
        self.sender = 'hamlet@zulip.com'
        self.recipient = 'cordelia@zulip.com'

    def _create_attachments(self):
        # type: () -> None
        sample_size = 10
        dummy_files = [
            ('zulip.txt', '1/31/4CBjtTLYZhk66pZrF8hnYGwc/zulip.txt', sample_size),
            ('temp_file.py', '1/31/4CBjtTLYZhk66pZrF8hnYGwc/temp_file.py', sample_size),
            ('abc.py', '1/31/4CBjtTLYZhk66pZrF8hnYGwc/abc.py', sample_size)
        ]
        user_profile = self.example_user('hamlet')
        for file_name, path_id, size in dummy_files:
            create_attachment(file_name, path_id, user_profile, size)

    def _check_messages_before_archiving(self, msg_id):
        # type: (int) -> List
        user_messages_ids_before = list(UserMessage.objects.filter(
            message_id=msg_id).order_by('id').values_list('id', flat=True))
        self.assertEqual(ArchivedUserMessage.objects.count(), 0)
        self.assertEqual(ArchivedMessage.objects.count(), 0)
        return user_messages_ids_before

    def _check_messages_after_archiving(self, msg_id, user_msgs_ids_before):
        # type: (int, List[int]) -> None
        self.assertEqual(ArchivedMessage.objects.filter(id=msg_id).count(), 1)
        self.assertEqual(Message.objects.filter(id=msg_id).count(), 0)
        self.assertEqual(UserMessage.objects.filter(message_id=msg_id).count(), 0)
        arc_user_messages_ids_after = list(ArchivedUserMessage.objects.filter(
            message_id=msg_id).order_by('id').values_list('id', flat=True))
        self.assertEqual(arc_user_messages_ids_after, user_msgs_ids_before)

    def test_personal_message_archiving(self):
        # type: ()-> None
        msg_id = self.send_message(self.sender, [self.recipient], Recipient.PERSONAL)
        user_messages_ids_before = self._check_messages_before_archiving(msg_id)
        move_message_to_archive(message_id=msg_id)
        self._check_messages_after_archiving(msg_id, user_messages_ids_before)

    def test_stream_message_archiving(self):
        # type: ()-> None
        msg_id = self.send_message(self.sender, "Verona", Recipient.STREAM)
        user_messages_ids_before = self._check_messages_before_archiving(msg_id)
        move_message_to_archive(message_id=msg_id)
        self._check_messages_after_archiving(msg_id, user_messages_ids_before)

    def test_archiving_message_second_time(self):
        # type: ()-> None
        msg_id = self.send_message(self.sender, "Verona", Recipient.STREAM)
        user_messages_ids_before = self._check_messages_before_archiving(msg_id)
        move_message_to_archive(message_id=msg_id)
        self._check_messages_after_archiving(msg_id, user_messages_ids_before)
        with self.assertRaises(Message.DoesNotExist):
            move_message_to_archive(message_id=msg_id)

    def test_archiving_message_with_attachment(self):
        # type: () -> None
        self._create_attachments()
        body = """Some files here ...[zulip.txt](
            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/zulip.txt)
            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/temp_file.py ....
            Some more.... http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/abc.py
        """
        msg_id = self.send_message(self.sender, [self.recipient], Recipient.PERSONAL, body)
        user_messages_ids_before = self._check_messages_before_archiving(msg_id)
        attachments_ids_before = list(Attachment.objects.filter(
            messages__id=msg_id).order_by("id").values_list("id", flat=True))
        self.assertEqual(ArchivedAttachment.objects.count(), 0)
        move_message_to_archive(message_id=msg_id)
        self._check_messages_after_archiving(msg_id, user_messages_ids_before)
        self.assertEqual(Attachment.objects.count(), 0)
        arc_attachments_ids_after = list(ArchivedAttachment.objects.filter(
            messages__id=msg_id).order_by("id").values_list("id", flat=True))
        self.assertEqual(attachments_ids_before, arc_attachments_ids_after)

    def test_archiving_message_with_shared_attachment(self):
        # type: () -> None
        # Check do not removing attachments which is used in other messages.
        self._create_attachments()
        body = """Some files here ...[zulip.txt](
            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/zulip.txt)
            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/temp_file.py ....
            Some more.... http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/abc.py
        """
        msg_id = self.send_message(self.sender, [self.recipient], Recipient.PERSONAL, body)
        msg_id_shared_attachments = self.send_message(self.recipient, [self.sender],
                                                      Recipient.PERSONAL, body)
        user_messages_ids_before = self._check_messages_before_archiving(msg_id)
        attachments_ids_before = list(Attachment.objects.filter(
            messages__id=msg_id).order_by("id").values_list("id", flat=True))
        self.assertEqual(ArchivedAttachment.objects.count(), 0)
        move_message_to_archive(message_id=msg_id)
        self._check_messages_after_archiving(msg_id, user_messages_ids_before)
        self.assertEqual(Attachment.objects.count(), 3)
        arc_attachments_ids_after = list(ArchivedAttachment.objects.filter(
            messages__id=msg_id).order_by("id").values_list("id", flat=True))
        self.assertEqual(attachments_ids_before, arc_attachments_ids_after)
        move_message_to_archive(message_id=msg_id_shared_attachments)
        self.assertEqual(Attachment.objects.count(), 0)
