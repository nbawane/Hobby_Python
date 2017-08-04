from __future__ import print_function

from typing import cast, Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Text

from confirmation.models import Confirmation
from django.conf import settings
from django.template import loader
from django.utils.timezone import now as timezone_now
from zerver.decorator import statsd_increment
from zerver.lib.send_email import send_future_email, display_email, \
    send_email_from_dict
from zerver.lib.queue import queue_json_publish
from zerver.models import (
    Recipient,
    ScheduledJob,
    UserMessage,
    Stream,
    get_display_recipient,
    UserProfile,
    get_user_profile_by_email,
    get_user_profile_by_id,
    receives_offline_notifications,
    get_context_for_message,
    Message,
    Realm,
)

import datetime
import re
import subprocess
import ujson
from six.moves import urllib
from collections import defaultdict

def unsubscribe_token(user_profile):
    # type: (UserProfile) -> Text
    # Leverage the Django confirmations framework to generate and track unique
    # unsubscription tokens.
    return Confirmation.objects.get_link_for_object(user_profile).split("/")[-1]

def one_click_unsubscribe_link(user_profile, endpoint):
    # type: (UserProfile, Text) -> Text
    """
    Generate a unique link that a logged-out user can visit to unsubscribe from
    Zulip e-mails without having to first log in.
    """
    token = unsubscribe_token(user_profile)
    resource_path = "accounts/unsubscribe/%s/%s" % (endpoint, token)
    return "%s/%s" % (user_profile.realm.uri.rstrip("/"), resource_path)

def hash_util_encode(string):
    # type: (Text) -> Text
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def pm_narrow_url(realm, participants):
    # type: (Realm, List[Text]) -> Text
    participants.sort()
    base_url = u"%s/#narrow/pm-with/" % (realm.uri,)
    return base_url + hash_util_encode(",".join(participants))

def stream_narrow_url(realm, stream):
    # type: (Realm, Text) -> Text
    base_url = u"%s/#narrow/stream/" % (realm.uri,)
    return base_url + hash_util_encode(stream)

def topic_narrow_url(realm, stream, topic):
    # type: (Realm, Text, Text) -> Text
    base_url = u"%s/#narrow/stream/" % (realm.uri,)
    return u"%s%s/topic/%s" % (base_url, hash_util_encode(stream),
                               hash_util_encode(topic))

def build_message_list(user_profile, messages):
    # type: (UserProfile, List[Message]) -> List[Dict[str, Any]]
    """
    Builds the message list object for the missed message email template.
    The messages are collapsed into per-recipient and per-sender blocks, like
    our web interface
    """
    messages_to_render = []  # type: List[Dict[str, Any]]

    def sender_string(message):
        # type: (Message) -> Text
        if message.recipient.type in (Recipient.STREAM, Recipient.HUDDLE):
            return message.sender.full_name
        else:
            return ''

    def relative_to_full_url(content):
        # type: (Text) -> Text
        # URLs for uploaded content are of the form
        # "/user_uploads/abc.png". Make them full paths.
        #
        # There's a small chance of colliding with non-Zulip URLs containing
        # "/user_uploads/", but we don't have much information about the
        # structure of the URL to leverage.
        content = re.sub(
            r"/user_uploads/(\S*)",
            user_profile.realm.uri + r"/user_uploads/\1", content)

        # Our proxying user-uploaded images seems to break inline images in HTML
        # emails, so scrub the image but leave the link.
        content = re.sub(
            r"<img src=(\S+)/user_uploads/(\S+)>", "", content)

        # URLs for emoji are of the form
        # "static/generated/emoji/images/emoji/snowflake.png".
        content = re.sub(
            r"/static/generated/emoji/images/emoji/",
            user_profile.realm.uri + r"/static/generated/emoji/images/emoji/",
            content)

        return content

    def fix_plaintext_image_urls(content):
        # type: (Text) -> Text
        # Replace image URLs in plaintext content of the form
        #     [image name](image url)
        # with a simple hyperlink.
        return re.sub(r"\[(\S*)\]\((\S*)\)", r"\2", content)

    def fix_emoji_sizes(html):
        # type: (Text) -> Text
        return html.replace(' class="emoji"', ' height="20px"')

    def build_message_payload(message):
        # type: (Message) -> Dict[str, Text]
        plain = message.content
        plain = fix_plaintext_image_urls(plain)
        plain = relative_to_full_url(plain)

        assert message.rendered_content is not None
        html = message.rendered_content
        html = relative_to_full_url(html)
        html = fix_emoji_sizes(html)

        return {'plain': plain, 'html': html}

    def build_sender_payload(message):
        # type: (Message) -> Dict[str, Any]
        sender = sender_string(message)
        return {'sender': sender,
                'content': [build_message_payload(message)]}

    def message_header(user_profile, message):
        # type: (UserProfile, Message) -> Dict[str, Any]
        disp_recipient = get_display_recipient(message.recipient)
        if message.recipient.type == Recipient.PERSONAL:
            header = u"You and %s" % (message.sender.full_name,)
            html_link = pm_narrow_url(user_profile.realm, [message.sender.email])
            header_html = u"<a style='color: #ffffff;' href='%s'>%s</a>" % (html_link, header)
        elif message.recipient.type == Recipient.HUDDLE:
            assert not isinstance(disp_recipient, Text)
            other_recipients = [r['full_name'] for r in disp_recipient
                                if r['email'] != user_profile.email]
            header = u"You and %s" % (", ".join(other_recipients),)
            html_link = pm_narrow_url(user_profile.realm, [r["email"] for r in disp_recipient
                                      if r["email"] != user_profile.email])
            header_html = u"<a style='color: #ffffff;' href='%s'>%s</a>" % (html_link, header)
        else:
            assert isinstance(disp_recipient, Text)
            header = u"%s > %s" % (disp_recipient, message.topic_name())
            stream_link = stream_narrow_url(user_profile.realm, disp_recipient)
            topic_link = topic_narrow_url(user_profile.realm, disp_recipient, message.subject)
            header_html = u"<a href='%s'>%s</a> > <a href='%s'>%s</a>" % (
                stream_link, disp_recipient, topic_link, message.subject)
        return {"plain": header,
                "html": header_html,
                "stream_message": message.recipient.type_name() == "stream"}

    # # Collapse message list to
    # [
    #    {
    #       "header": {
    #                   "plain":"header",
    #                   "html":"htmlheader"
    #                 }
    #       "senders":[
    #          {
    #             "sender":"sender_name",
    #             "content":[
    #                {
    #                   "plain":"content",
    #                   "html":"htmlcontent"
    #                }
    #                {
    #                   "plain":"content",
    #                   "html":"htmlcontent"
    #                }
    #             ]
    #          }
    #       ]
    #    },
    # ]

    messages.sort(key=lambda message: message.pub_date)

    for message in messages:
        header = message_header(user_profile, message)

        # If we want to collapse into the previous recipient block
        if len(messages_to_render) > 0 and messages_to_render[-1]['header'] == header:
            sender = sender_string(message)
            sender_block = messages_to_render[-1]['senders']

            # Same message sender, collapse again
            if sender_block[-1]['sender'] == sender:
                sender_block[-1]['content'].append(build_message_payload(message))
            else:
                # Start a new sender block
                sender_block.append(build_sender_payload(message))
        else:
            # New recipient and sender block
            recipient_block = {'header': header,
                               'senders': [build_sender_payload(message)]}

            messages_to_render.append(recipient_block)

    return messages_to_render

@statsd_increment("missed_message_reminders")
def do_send_missedmessage_events_reply_in_zulip(user_profile, missed_messages, message_count):
    # type: (UserProfile, List[Message], int) -> None
    """
    Send a reminder email to a user if she's missed some PMs by being offline.

    The email will have its reply to address set to a limited used email
    address that will send a zulip message to the correct recipient. This
    allows the user to respond to missed PMs, huddles, and @-mentions directly
    from the email.

    `user_profile` is the user to send the reminder to
    `missed_messages` is a list of Message objects to remind about they should
                      all have the same recipient and subject
    """
    from zerver.context_processors import common_context
    # Disabled missedmessage emails internally
    if not user_profile.enable_offline_email_notifications:
        return

    recipients = set((msg.recipient_id, msg.subject) for msg in missed_messages)
    if len(recipients) != 1:
        raise ValueError(
            'All missed_messages must have the same recipient and subject %r' %
            recipients
        )

    unsubscribe_link = one_click_unsubscribe_link(user_profile, "missed_messages")
    context = common_context(user_profile)
    context.update({
        'name': user_profile.full_name,
        'messages': build_message_list(user_profile, missed_messages),
        'message_count': message_count,
        'mention': missed_messages[0].recipient.type == Recipient.STREAM,
        'unsubscribe_link': unsubscribe_link,
    })

    # If this setting (email mirroring integration) is enabled, only then
    # can users reply to email to send message to Zulip. Thus, one must
    # ensure to display warning in the template.
    if settings.EMAIL_GATEWAY_PATTERN:
        context.update({
            'reply_warning': False,
            'reply_to_zulip': True,
        })
    else:
        context.update({
            'reply_warning': True,
            'reply_to_zulip': False,
        })

    from zerver.lib.email_mirror import create_missed_message_address
    address = create_missed_message_address(user_profile, missed_messages[0])

    senders = list(set(m.sender for m in missed_messages))
    if (missed_messages[0].recipient.type == Recipient.HUDDLE):
        display_recipient = get_display_recipient(missed_messages[0].recipient)
        # Make sure that this is a list of strings, not a string.
        assert not isinstance(display_recipient, Text)
        other_recipients = [r['full_name'] for r in display_recipient
                            if r['id'] != user_profile.id]
        context.update({'group_pm': True})
        if len(other_recipients) == 2:
            huddle_display_name = u"%s" % (" and ".join(other_recipients))
            context.update({'huddle_display_name': huddle_display_name})
        elif len(other_recipients) == 3:
            huddle_display_name = u"%s, %s, and %s" % (other_recipients[0], other_recipients[1], other_recipients[2])
            context.update({'huddle_display_name': huddle_display_name})
        else:
            huddle_display_name = u"%s, and %s others" % (', '.join(other_recipients[:2]), len(other_recipients) - 2)
            context.update({'huddle_display_name': huddle_display_name})
    elif (missed_messages[0].recipient.type == Recipient.PERSONAL):
        context.update({'private_message': True})
    else:
        # Keep only the senders who actually mentioned the user
        #
        # TODO: When we add wildcard mentions that send emails, add
        # them to the filter here.
        senders = list(set(m.sender for m in missed_messages if
                           UserMessage.objects.filter(message=m, user_profile=user_profile,
                                                      flags=UserMessage.flags.mentioned).exists()))
        context.update({'at_mention': True})

    context.update({
        'sender_str': ", ".join(sender.full_name for sender in senders),
        'realm_str': user_profile.realm.name,
    })

    from_email = None

    if len(senders) == 1 and settings.SEND_MISSED_MESSAGE_EMAILS_AS_USER:
        # If this setting is enabled, you can reply to the Zulip
        # missed message emails directly back to the original sender.
        # However, one must ensure the Zulip server is in the SPF
        # record for the domain, or there will be spam/deliverability
        # problems.
        sender = senders[0]
        from_email = '"%s" <%s>' % (sender.full_name, sender.email)
        context.update({
            'reply_warning': False,
            'reply_to_zulip': False,
        })

    email_dict = {
        'template_prefix': 'zerver/emails/missed_message',
        'to_email': display_email(user_profile),
        'from_email': from_email,
        'reply_to_email': address,
        'context': context}
    queue_json_publish("missedmessage_email_senders", email_dict, send_email_from_dict)

    user_profile.last_reminder = timezone_now()
    user_profile.save(update_fields=['last_reminder'])

def handle_missedmessage_emails(user_profile_id, missed_email_events):
    # type: (int, Iterable[Dict[str, Any]]) -> None
    message_ids = [event.get('message_id') for event in missed_email_events]

    user_profile = get_user_profile_by_id(user_profile_id)
    if not receives_offline_notifications(user_profile):
        return

    messages = Message.objects.filter(usermessage__user_profile_id=user_profile,
                                      id__in=message_ids,
                                      usermessage__flags=~UserMessage.flags.read)

    # Cancel missed-message emails for deleted messages
    messages = [um for um in messages if um.content != "(deleted)"]

    if not messages:
        return

    messages_by_recipient_subject = defaultdict(list)  # type: Dict[Tuple[int, Text], List[Message]]
    for msg in messages:
        messages_by_recipient_subject[(msg.recipient_id, msg.topic_name())].append(msg)

    message_count_by_recipient_subject = {
        recipient_subject: len(msgs)
        for recipient_subject, msgs in messages_by_recipient_subject.items()
    }

    for msg_list in messages_by_recipient_subject.values():
        msg = min(msg_list, key=lambda msg: msg.pub_date)
        if msg.recipient.type == Recipient.STREAM:
            msg_list.extend(get_context_for_message(msg))

    # Send an email per recipient subject pair
    for recipient_subject, msg_list in messages_by_recipient_subject.items():
        unique_messages = {m.id: m for m in msg_list}
        do_send_missedmessage_events_reply_in_zulip(
            user_profile,
            list(unique_messages.values()),
            message_count_by_recipient_subject[recipient_subject],
        )

def clear_followup_emails_queue(email):
    # type: (Text) -> None
    """
    Clear out queued emails that would otherwise be sent to a specific email address.
    """
    items = ScheduledJob.objects.filter(type=ScheduledJob.EMAIL, filter_string__iexact = email)
    items.delete()

def log_digest_event(msg):
    # type: (Text) -> None
    import logging
    logging.basicConfig(filename=settings.DIGEST_LOG_PATH, level=logging.INFO)
    logging.info(msg)

def enqueue_welcome_emails(email, name):
    # type: (Text, Text) -> None
    from zerver.context_processors import common_context
    if settings.WELCOME_EMAIL_SENDER is not None:
        # line break to avoid triggering lint rule
        from_email = '%(name)s <%(email)s>' % \
                     settings.WELCOME_EMAIL_SENDER
    else:
        from_email = settings.ZULIP_ADMINISTRATOR

    user_profile = get_user_profile_by_email(email)
    unsubscribe_link = one_click_unsubscribe_link(user_profile, "welcome")
    context = common_context(user_profile)
    context.update({
        'verbose_support_offers': settings.VERBOSE_SUPPORT_OFFERS,
        'unsubscribe_link': unsubscribe_link
    })
    send_future_email(
        "zerver/emails/followup_day1", '%s <%s>' % (name, email),
        from_email=from_email, context=context, delay=datetime.timedelta(hours=1))
    send_future_email(
        "zerver/emails/followup_day2", '%s <%s>' % (name, email),
        from_email=from_email, context=context, delay=datetime.timedelta(days=1))

def convert_html_to_markdown(html):
    # type: (Text) -> Text
    # On Linux, the tool installs as html2markdown, and there's a command called
    # html2text that does something totally different. On OSX, the tool installs
    # as html2text.
    commands = ["html2markdown", "html2text"]

    for command in commands:
        try:
            # A body width of 0 means do not try to wrap the text for us.
            p = subprocess.Popen(
                [command, "--body-width=0"], stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            break
        except OSError:
            continue

    markdown = p.communicate(input=html.encode('utf-8'))[0].decode('utf-8').strip()
    # We want images to get linked and inline previewed, but html2text will turn
    # them into links of the form `![](http://foo.com/image.png)`, which is
    # ugly. Run a regex over the resulting description, turning links of the
    # form `![](http://foo.com/image.png?12345)` into
    # `[image.png](http://foo.com/image.png)`.
    return re.sub(u"!\\[\\]\\((\\S*)/(\\S*)\\?(\\S*)\\)",
                  u"[\\2](\\1/\\2)", markdown)
