from __future__ import absolute_import

from typing import Text, Union, List, Dict
import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import has_request_variables, REQ, require_realm_admin
from zerver.lib.actions import (try_add_realm_custom_profile_field,
                                do_remove_realm_custom_profile_field,
                                try_update_realm_custom_profile_field,
                                do_update_user_custom_profile_data)
from zerver.lib.response import json_success, json_error
from zerver.lib.validator import check_dict, check_list, check_int

from zerver.models import (custom_profile_fields_for_realm, UserProfile,
                           CustomProfileField, custom_profile_fields_for_realm)

def list_realm_custom_profile_fields(request, user_profile):
    # type: (HttpRequest, UserProfile) -> HttpResponse
    fields = custom_profile_fields_for_realm(user_profile.realm_id)
    return json_success({'custom_fields': [f.as_dict() for f in fields]})

@require_realm_admin
@has_request_variables
def create_realm_custom_profile_field(request, user_profile, name=REQ(),
                                      field_type=REQ(validator=check_int)):
    # type: (HttpRequest, UserProfile, Text, int) -> HttpResponse
    if not name.strip():
        return json_error(_("Name cannot be blank."))

    if field_type not in CustomProfileField.FIELD_VALIDATORS:
        return json_error(_("Invalid field type."))

    try:
        field = try_add_realm_custom_profile_field(
            realm=user_profile.realm,
            name=name,
            field_type=field_type,
        )
        return json_success({'id': field.id})
    except IntegrityError:
        return json_error(_("A field with that name already exists."))

@require_realm_admin
def delete_realm_custom_profile_field(request, user_profile, field_id):
    # type: (HttpRequest, UserProfile, int) -> HttpResponse
    try:
        field = CustomProfileField.objects.get(id=field_id)
    except CustomProfileField.DoesNotExist:
        return json_error(_('Field id {id} not found.').format(id=field_id))

    do_remove_realm_custom_profile_field(realm=user_profile.realm,
                                         field=field)
    return json_success()

@require_realm_admin
@has_request_variables
def update_realm_custom_profile_field(request, user_profile, field_id,
                                      name=REQ()):
    # type: (HttpRequest, UserProfile, int, Text) -> HttpResponse
    if not name.strip():
        return json_error(_("Name cannot be blank."))

    realm = user_profile.realm
    try:
        field = CustomProfileField.objects.get(realm=realm, id=field_id)
    except CustomProfileField.DoesNotExist:
        return json_error(_('Field id {id} not found.').format(id=field_id))

    try:
        try_update_realm_custom_profile_field(realm, field, name)
    except IntegrityError:
        return json_error(_('A field with that name already exists.'))
    return json_success()

@has_request_variables
def update_user_custom_profile_data(
        request,
        user_profile,
        data=REQ(validator=check_list(check_dict([('id', check_int)])))):
    # type: (HttpRequest, UserProfile, List[Dict[str, Union[int, Text]]]) -> HttpResponse
    for item in data:
        field_id = item['id']
        try:
            field = CustomProfileField.objects.get(id=field_id)
        except CustomProfileField.DoesNotExist:
            return json_error(_('Field id {id} not found.').format(id=field_id))

        validator = CustomProfileField.FIELD_VALIDATORS[field.field_type]
        result = validator('value[{}]'.format(field_id), item['value'])
        if result is not None:
            return json_error(result)

    do_update_user_custom_profile_data(user_profile, data)
    # We need to call this explicitly otherwise constraints are not check
    return json_success()
