# -*- coding: utf-8 -*-
from __future__ import absolute_import

from zerver.lib.actions import get_realm, check_add_realm_emoji
from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.test_helpers import get_test_image_file, get_user_profile_by_email
from zerver.models import RealmEmoji
import ujson

class RealmEmojiTest(ZulipTestCase):

    def test_list(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        realm = get_realm('zulip')
        check_add_realm_emoji(realm, "my_emoji", "my_emoji")
        result = self.client_get("/json/realm/emoji")
        self.assert_json_success(result)
        self.assertEqual(200, result.status_code)
        content = ujson.loads(result.content)
        self.assertEqual(len(content["emoji"]), 1)

    def test_list_no_author(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        realm = get_realm('zulip')
        RealmEmoji.objects.create(realm=realm, name='my_emojy', file_name='my_emojy')
        result = self.client_get("/json/realm/emoji")
        self.assert_json_success(result)
        content = ujson.loads(result.content)
        self.assertEqual(len(content["emoji"]), 1)
        self.assertIsNone(content["emoji"]['my_emojy']['author'])

    def test_list_admins_only(self):
        # type: () -> None
        email = self.example_email('othello')
        self.login(email)
        realm = get_realm('zulip')
        realm.add_emoji_by_admins_only = True
        realm.save()
        check_add_realm_emoji(realm, 'my_emojy', 'my_emojy')
        result = self.client_get("/json/realm/emoji")
        self.assert_json_success(result)
        content = ujson.loads(result.content)
        self.assertEqual(len(content["emoji"]), 1)
        self.assertIsNone(content["emoji"]['my_emojy']['author'])

    def test_upload(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp1:
            emoji_data = {'f1': fp1}
            result = self.client_put_multipart('/json/realm/emoji/my_emoji', info=emoji_data)
        self.assert_json_success(result)
        self.assertEqual(200, result.status_code)
        emoji = RealmEmoji.objects.get(name="my_emoji")
        self.assertEqual(emoji.author.email, email)

        result = self.client_get("/json/realm/emoji")
        content = ujson.loads(result.content)
        self.assert_json_success(result)
        self.assertEqual(len(content["emoji"]), 1)
        self.assertIn('author', content["emoji"]['my_emoji'])
        self.assertEqual(
            content["emoji"]['my_emoji']['author']['email'], email)

        realm_emoji = RealmEmoji.objects.get(realm=get_realm('zulip'))
        self.assertEqual(
            str(realm_emoji),
            '<RealmEmoji(zulip): my_emoji my_emoji.png>'
        )

    def test_upload_exception(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp1:
            emoji_data = {'f1': fp1}
            result = self.client_put_multipart('/json/realm/emoji/my_em*oji', info=emoji_data)
        self.assert_json_error(result, 'Invalid characters in emoji name')

    def test_upload_uppercase_exception(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp1:
            emoji_data = {'f1': fp1}
            result = self.client_put_multipart('/json/realm/emoji/my_EMoji', info=emoji_data)
        self.assert_json_error(result, 'Invalid characters in emoji name')

    def test_upload_admins_only(self):
        # type: () -> None
        email = self.example_email('othello')
        self.login(email)
        realm = get_realm('zulip')
        realm.add_emoji_by_admins_only = True
        realm.save()
        with get_test_image_file('img.png') as fp1:
            emoji_data = {'f1': fp1}
            result = self.client_put_multipart('/json/realm/emoji/my_emoji', info=emoji_data)
        self.assert_json_error(result, 'Must be a realm administrator')

    def test_delete(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        realm = get_realm('zulip')
        check_add_realm_emoji(realm, "my_emoji", "my_emoji.png")
        result = self.client_delete("/json/realm/emoji/my_emoji")
        self.assert_json_success(result)

        result = self.client_get("/json/realm/emoji")
        content = ujson.loads(result.content)
        self.assert_json_success(result)
        self.assertEqual(len(content["emoji"]), 0)

    def test_delete_admins_only(self):
        # type: () -> None
        email = self.example_email('othello')
        self.login(email)
        realm = get_realm('zulip')
        realm.add_emoji_by_admins_only = True
        realm.save()
        check_add_realm_emoji(realm, "my_emoji", "my_emoji.png")
        result = self.client_delete("/json/realm/emoji/my_emoji")
        self.assert_json_error(result, 'Must be a realm administrator')

    def test_delete_admin_or_author(self):
        # type: () -> None
        # If any user in a realm can upload the emoji then the user who
        # uploaded it as well as the admin should be able to delete it.
        author = get_user_profile_by_email('othello@zulip.com')
        realm = get_realm('zulip')
        realm.add_emoji_by_admins_only = False
        realm.save()
        check_add_realm_emoji(realm, "my_emoji", "my_emoji.png", author)
        self.login('othello@zulip.com')
        result = self.client_delete("/json/realm/emoji/my_emoji")
        self.assert_json_success(result)
        self.logout()

        check_add_realm_emoji(realm, "my_emoji", "my_emoji.png", author)
        self.login('iago@zulip.com')
        result = self.client_delete("/json/realm/emoji/my_emoji")
        self.assert_json_success(result)
        self.logout()

        check_add_realm_emoji(realm, "my_emoji", "my_emoji.png", author)
        self.login('cordelia@zulip.com')
        result = self.client_delete("/json/realm/emoji/my_emoji")
        self.assert_json_error(result, 'Must be a realm administrator or emoji author')

    def test_delete_exception(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        result = self.client_delete("/json/realm/emoji/invalid_emoji")
        self.assert_json_error(result, "Emoji 'invalid_emoji' does not exist")

    def test_multiple_upload(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp1, get_test_image_file('img.png') as fp2:
            result = self.client_put_multipart('/json/realm/emoji/my_emoji', {'f1': fp1, 'f2': fp2})
        self.assert_json_error(result, 'You must upload exactly one file.')

    def test_emoji_upload_file_size_error(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp:
            with self.settings(MAX_EMOJI_FILE_SIZE=0):
                result = self.client_put_multipart('/json/realm/emoji/my_emoji', {'file': fp})
        self.assert_json_error(result, 'Uploaded file is larger than the allowed limit of 0 MB')

    def test_upload_already_existed_emoji(self):
        # type: () -> None
        email = self.example_email('iago')
        self.login(email)
        with get_test_image_file('img.png') as fp1:
            emoji_data = {'f1': fp1}
            self.client_put_multipart('/json/realm/emoji/my_emoji', info=emoji_data)
        with get_test_image_file('img.png') as fp1:
                emoji_data = {'f1': fp1}
                result = self.client_put_multipart('/json/realm/emoji/my_emoji', info=emoji_data)
        self.assert_json_error(result, 'Realm emoji with this Realm and Name already exists.')
