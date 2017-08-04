# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from typing import Optional, Text

from zerver.lib.actions import do_change_is_admin, \
    do_change_realm_domain, do_create_realm, \
    do_remove_realm_domain
from zerver.lib.domains import validate_domain
from zerver.lib.test_classes import ZulipTestCase
from zerver.models import email_allowed_for_realm, get_realm, \
    get_realm_by_email_domain, \
    GetRealmByDomainException, RealmDomain

import ujson


class RealmDomainTest(ZulipTestCase):
    def test_list_realm_domains(self):
        # type: () -> None
        self.login(self.example_email("iago"))
        realm = get_realm('zulip')
        RealmDomain.objects.create(realm=realm, domain='acme.com', allow_subdomains=True)
        result = self.client_get("/json/realm/domains")
        self.assert_json_success(result)
        received = ujson.dumps(ujson.loads(result.content)['domains'], sort_keys=True)
        expected = ujson.dumps([{'domain': 'zulip.com', 'allow_subdomains': False},
                                {'domain': 'acme.com', 'allow_subdomains': True}],
                               sort_keys=True)
        self.assertEqual(received, expected)

    def test_not_realm_admin(self):
        # type: () -> None
        self.login(self.example_email("hamlet"))
        result = self.client_post("/json/realm/domains")
        self.assert_json_error(result, 'Must be a realm administrator')
        result = self.client_patch("/json/realm/domains/15")
        self.assert_json_error(result, 'Must be a realm administrator')
        result = self.client_delete("/json/realm/domains/15")
        self.assert_json_error(result, 'Must be a realm administrator')

    def test_create_realm_domain(self):
        # type: () -> None
        self.login(self.example_email("iago"))
        data = {'domain': ujson.dumps(''),
                'allow_subdomains': ujson.dumps(True)}
        result = self.client_post("/json/realm/domains", info=data)
        self.assert_json_error(result, 'Invalid domain: Domain can\'t be empty.')

        data['domain'] = ujson.dumps('acme.com')
        result = self.client_post("/json/realm/domains", info=data)
        self.assert_json_success(result)
        realm = get_realm('zulip')
        self.assertTrue(RealmDomain.objects.filter(realm=realm, domain='acme.com',
                                                   allow_subdomains=True).exists())

        result = self.client_post("/json/realm/domains", info=data)
        self.assert_json_error(result, 'The domain acme.com is already a part of your organization.')

        mit_user_profile = self.mit_user("sipbtest")
        self.login(mit_user_profile.email)

        do_change_is_admin(mit_user_profile, True)
        result = self.client_post("/json/realm/domains", info=data)
        self.assert_json_error(result, 'The domain acme.com belongs to another organization.')
        with self.settings(REALMS_HAVE_SUBDOMAINS=True):
            result = self.client_post("/json/realm/domains", info=data,
                                      HTTP_HOST=mit_user_profile.realm.host)
            self.assert_json_success(result)

    def test_patch_realm_domain(self):
        # type: () -> None
        self.login(self.example_email("iago"))
        realm = get_realm('zulip')
        RealmDomain.objects.create(realm=realm, domain='acme.com',
                                   allow_subdomains=False)
        data = {
            'allow_subdomains': ujson.dumps(True),
        }
        url = "/json/realm/domains/acme.com"
        result = self.client_patch(url, data)
        self.assert_json_success(result)
        self.assertTrue(RealmDomain.objects.filter(realm=realm, domain='acme.com',
                                                   allow_subdomains=True).exists())

        url = "/json/realm/domains/non-existent.com"
        result = self.client_patch(url, data)
        self.assertEqual(result.status_code, 400)
        self.assert_json_error(result, 'No entry found for domain non-existent.com.')

    def test_delete_realm_domain(self):
        # type: () -> None
        self.login(self.example_email("iago"))
        realm = get_realm('zulip')
        RealmDomain.objects.create(realm=realm, domain='acme.com')
        result = self.client_delete("/json/realm/domains/non-existent.com")
        self.assertEqual(result.status_code, 400)
        self.assert_json_error(result, 'No entry found for domain non-existent.com.')

        result = self.client_delete("/json/realm/domains/acme.com")
        self.assert_json_success(result)
        self.assertFalse(RealmDomain.objects.filter(domain='acme.com').exists())
        self.assertTrue(realm.restricted_to_domain)

    def test_delete_all_realm_domains(self):
        # type: () -> None
        self.login(self.example_email("iago"))
        realm = get_realm('zulip')
        query = RealmDomain.objects.filter(realm=realm)

        self.assertTrue(realm.restricted_to_domain)
        for realm_domain in query.all():
            do_remove_realm_domain(realm_domain)
        self.assertEqual(query.count(), 0)
        # Deleting last realm_domain should set `restricted_to_domain` to False.
        # This should be tested on a fresh instance, since the cached objects
        # would not be updated.
        self.assertFalse(get_realm('zulip').restricted_to_domain)

    def test_get_realm_by_email_domain(self):
        # type: () -> None
        realm1, created = do_create_realm('testrealm1', 'Test Realm 1')
        realm2, created = do_create_realm('testrealm2', 'Test Realm 2')
        realm3, created = do_create_realm('testrealm3', 'Test Realm 3')

        realm_domain_1 = RealmDomain.objects.create(realm=realm1, domain='test1.com', allow_subdomains=True)
        realm_domain_2 = RealmDomain.objects.create(realm=realm2, domain='test2.test1.com', allow_subdomains=False)
        RealmDomain.objects.create(realm=realm3, domain='test3.test2.test1.com', allow_subdomains=True)

        def assert_and_check(email, realm_string_id):
            # type: (Text, Optional[Text]) -> None
            realm = get_realm_by_email_domain(email)
            if realm_string_id is None:
                self.assertIsNone(realm)
            else:
                assert(realm is not None)
                self.assertEqual(realm.string_id, realm_string_id)

        assert_and_check('user@zulip.com', 'zulip')
        assert_and_check('user@fakedomain.com', None)
        assert_and_check('user@test1.com', 'testrealm1')
        assert_and_check('user@test2.test1.com', 'testrealm2')
        assert_and_check('user@test3.test2.test1.com', 'testrealm3')
        assert_and_check('user@test2.test1.com', 'testrealm2')
        assert_and_check('user@test2.test2.test1.com', 'testrealm1')
        assert_and_check('user@test1.test3.test2.test1.com', 'testrealm3')

        do_change_realm_domain(realm_domain_1, False)
        assert_and_check('user@test1.test1.com', None)
        assert_and_check('user@test1.com', 'testrealm1')

        do_change_realm_domain(realm_domain_2, True)
        assert_and_check('user@test2.test1.com', 'testrealm2')
        assert_and_check('user@test2.test2.test1.com', 'testrealm2')

        with self.settings(REALMS_HAVE_SUBDOMAINS = True), (
                self.assertRaises(GetRealmByDomainException)):
            get_realm_by_email_domain('user@zulip.com')

    def test_email_allowed_for_realm(self):
        # type: () -> None
        realm1, created = do_create_realm('testrealm1', 'Test Realm 1', restricted_to_domain=True)
        realm2, created = do_create_realm('testrealm2', 'Test Realm 2', restricted_to_domain=True)

        realm_domain = RealmDomain.objects.create(realm=realm1, domain='test1.com', allow_subdomains=False)
        RealmDomain.objects.create(realm=realm2, domain='test2.test1.com', allow_subdomains=True)

        self.assertEqual(email_allowed_for_realm('user@test1.com', realm1), True)
        self.assertEqual(email_allowed_for_realm('user@test2.test1.com', realm1), False)
        self.assertEqual(email_allowed_for_realm('user@test2.test1.com', realm2), True)
        self.assertEqual(email_allowed_for_realm('user@test3.test2.test1.com', realm2), True)
        self.assertEqual(email_allowed_for_realm('user@test3.test1.com', realm2), False)

        do_change_realm_domain(realm_domain, True)
        self.assertEqual(email_allowed_for_realm('user@test1.com', realm1), True)
        self.assertEqual(email_allowed_for_realm('user@test2.test1.com', realm1), True)
        self.assertEqual(email_allowed_for_realm('user@test2.com', realm1), False)

    def test_realm_realm_domains_uniqueness(self):
        # type: () -> None
        realm = get_realm('zulip')
        with self.settings(REALMS_HAVE_SUBDOMAINS=True), self.assertRaises(IntegrityError):
            RealmDomain.objects.create(realm=realm, domain='zulip.com', allow_subdomains=True)

    def test_validate_domain(self):
        # type: () -> None
        invalid_domains = ['', 'test', 't.', 'test.', '.com', '-test', 'test...com',
                           'test-', 'test_domain.com', 'test.-domain.com']
        for domain in invalid_domains:
            with self.assertRaises(ValidationError):
                validate_domain(domain)

        valid_domains = ['acme.com', 'x-x.y.3.z']
        for domain in valid_domains:
            validate_domain(domain)
