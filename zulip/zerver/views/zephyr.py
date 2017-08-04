from __future__ import absolute_import
from typing import Any, List, Dict, Optional, Callable, Tuple, Iterable, Sequence, Text

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.utils.translation import ugettext as _
from zerver.decorator import authenticated_json_view
from zerver.lib.ccache import make_ccache
from zerver.lib.request import has_request_variables, REQ, JsonableError
from zerver.lib.response import json_success, json_error
from zerver.lib.str_utils import force_str
from zerver.models import UserProfile

import base64
import logging
import subprocess
import ujson


# Hack for mit.edu users whose Kerberos usernames don't match what they zephyr
# as.  The key is for Kerberos and the value is for zephyr.
kerberos_alter_egos = {
    'golem': 'ctl',
}

@authenticated_json_view
@has_request_variables
def webathena_kerberos_login(request, user_profile,
                             cred=REQ(default=None)):
    # type: (HttpRequest, UserProfile, Text) -> HttpResponse
    global kerberos_alter_egos
    if cred is None:
        return json_error(_("Could not find Kerberos credential"))
    if not user_profile.realm.webathena_enabled:
        return json_error(_("Webathena login not enabled"))

    try:
        parsed_cred = ujson.loads(cred)
        user = parsed_cred["cname"]["nameString"][0]
        if user in kerberos_alter_egos:
            user = kerberos_alter_egos[user]
        assert(user == user_profile.email.split("@")[0])
        ccache = make_ccache(parsed_cred)
    except Exception:
        return json_error(_("Invalid Kerberos cache"))

    # TODO: Send these data via (say) rabbitmq
    try:
        subprocess.check_call(["ssh", settings.PERSONAL_ZMIRROR_SERVER, "--",
                               "/home/zulip/zulip/api/integrations/zephyr/process_ccache",
                               force_str(user),
                               force_str(user_profile.api_key),
                               force_str(base64.b64encode(ccache))])
    except Exception:
        logging.exception("Error updating the user's ccache")
        return json_error(_("We were unable to setup mirroring for you"))

    return json_success()
