var compose = (function () {

var exports = {};

/* Track the state of the @all warning. The user must acknowledge that they are spamming the entire
   stream before the warning will go away. If they try to send before explicitly dismissing the
   warning, they will get an error message too.

   undefined: no @all/@everyone in message;
   false: user typed @all/@everyone;
   true: user clicked YES */

var user_acknowledged_all_everyone;

exports.all_everyone_warn_threshold = 15;

var uploads_domain = document.location.protocol + '//' + document.location.host;
var uploads_path = '/user_uploads';
var uploads_re = new RegExp("\\]\\(" + uploads_domain + "(" + uploads_path + "[^\\)]+)\\)", 'g');

function make_upload_absolute(uri) {
    if (uri.indexOf(uploads_path) === 0) {
        // Rewrite the URI to a usable link
        return uploads_domain + uri;
    }
    return uri;
}

function make_uploads_relative(content) {
    // Rewrite uploads in markdown links back to domain-relative form
    return content.replace(uploads_re, "]($1)");
}

// This function resets an input type="file".  Pass in the
// jquery object.
function clear_out_file_list(jq_file_list) {
    var clone_for_ie_sake = jq_file_list.clone(true);
    jq_file_list.replaceWith(clone_for_ie_sake);

    // Hack explanation:
    // IE won't let you do this (untested, but so says StackOverflow):
    //    $("#file_input").val("");
}

function show_all_everyone_warnings() {
    var current_stream = stream_data.get_sub(compose_state.stream_name());
    var stream_count = current_stream.subscribers.num_items();

    var all_everyone_template = templates.render("compose_all_everyone", {count: stream_count});
    var error_area_all_everyone = $("#compose-all-everyone");

    // only show one error for any number of @all or @everyone mentions
    if (!error_area_all_everyone.is(':visible')) {
        error_area_all_everyone.append(all_everyone_template);
    }

    error_area_all_everyone.show();
    user_acknowledged_all_everyone = false;
}

exports.clear_all_everyone_warnings = function () {
    $("#compose-all-everyone").hide();
    $("#compose-all-everyone").empty();
    $("#send-status").hide();
};

exports.clear_invites = function () {
    $("#compose_invite_users").hide();
    $("#compose_invite_users").empty();
};

exports.reset_user_acknowledged_all_everyone_flag = function () {
    user_acknowledged_all_everyone = undefined;
};

exports.clear_preview_area = function () {
    $("#new_message_content").show();
    $("#undo_markdown_preview").hide();
    $("#preview_message_area").hide();
    $("#preview_content").empty();
    $("#markdown_preview").show();
};

function update_fade() {
    if (!compose_state.composing()) {
        return;
    }

    var msg_type = compose_state.get_message_type();
    compose_fade.set_focused_recipient(msg_type);
    compose_fade.update_faded_messages();
}

$(function () {
    $('#stream,#subject,#private_message_recipient').bind({
         keyup: update_fade,
         change: update_fade,
    });
});

exports.abort_xhr = function () {
    $("#compose-send-button").removeAttr("disabled");
    var xhr = $("#compose").data("filedrop_xhr");
    if (xhr !== undefined) {
        xhr.abort();
        $("#compose").removeData("filedrop_xhr");
    }
};

exports.empty_topic_placeholder = function () {
    return i18n.t("(no topic)");
};

function create_message_object() {
    // Subjects are optional, and we provide a placeholder if one isn't given.
    var subject = compose_state.subject();
    if (subject === "") {
        subject = compose.empty_topic_placeholder();
    }

    var content = make_uploads_relative(compose_state.message_content());

    // Changes here must also be kept in sync with echo.try_deliver_locally
    var message = {
        type: compose_state.get_message_type(),
        content: content,
        sender_id: page_params.user_id,
        queue_id: page_params.queue_id,
        stream: '',
        subject: '',
    };

    if (message.type === "private") {
        // TODO: this should be collapsed with the code in composebox_typeahead.js
        var recipient = compose_state.recipient();
        var emails = util.extract_pm_recipients(recipient);
        message.to = emails;
        message.reply_to = recipient;
        message.private_message_recipient = recipient;
        message.to_user_ids = people.email_list_to_user_ids_string(emails);
    } else {
        var stream_name = compose_state.stream_name();
        message.to = stream_name;
        message.stream = stream_name;
        var sub = stream_data.get_sub(stream_name);
        if (sub) {
            message.stream_id = sub.stream_id;
        }
        message.subject = subject;
    }
    return message;
}
// Export for testing
exports.create_message_object = create_message_object;

function compose_error(error_text, bad_input) {
    $('#send-status').removeClass(status_classes)
               .addClass('alert-error')
               .stop(true).fadeTo(0, 1);
    $('#error-msg').html(error_text);
    $("#compose-send-button").removeAttr('disabled');
    $("#sending-indicator").hide();
    if (bad_input !== undefined) {
        bad_input.focus().select();
    }
}

function send_message_ajax(request, success, error) {
    channel.post({
        url: '/json/messages',
        data: request,
        success: success,
        error: function (xhr, error_type) {
            if (error_type !== 'timeout' && reload.is_pending()) {
                // The error might be due to the server changing
                reload.initiate({immediate: true,
                                 save_pointer: true,
                                 save_narrow: true,
                                 save_compose: true,
                                 send_after_reload: true});
                return;
            }

            var response = channel.xhr_error_message("Error sending message", xhr);
            error(response);
        },
    });
}

function report_send_time(send_time, receive_time, display_time, locally_echoed, rendered_changed) {
    var data = {time: send_time.toString(),
                received: receive_time.toString(),
                displayed: display_time.toString(),
                locally_echoed: locally_echoed};
    if (locally_echoed) {
        data.rendered_content_disparity = rendered_changed;
    }
    channel.post({
        url: '/json/report_send_time',
        data: data,
    });
}

var socket;
if (page_params.use_websockets) {
    socket = new Socket("/sockjs");
}
// For debugging.  The socket will eventually move out of this file anyway.
exports._socket = socket;

function send_message_socket(request, success, error) {
    request.socket_user_agent = navigator.userAgent;
    socket.send(request, success, function (type, resp) {
        var err_msg = "Error sending message";
        if (type === 'response') {
            err_msg += ": " + resp.msg;
        }
        error(err_msg);
    });
}

exports.send_times_log = [];
exports.send_times_data = {};
function maybe_report_send_times(message_id) {
    var data = exports.send_times_data[message_id];
    if (data.send_finished === undefined || data.received === undefined ||
        data.displayed === undefined) {
        // We report the data once we have both the send and receive times
        return;
    }
    report_send_time(data.send_finished - data.start,
                     data.received - data.start,
                     data.displayed - data.start,
                     data.locally_echoed,
                     data.rendered_content_disparity || false);
}

function mark_end_to_end_receive_time(message_id) {
    if (exports.send_times_data[message_id] === undefined) {
        exports.send_times_data[message_id] = {};
    }
    exports.send_times_data[message_id].received = new Date();
    maybe_report_send_times(message_id);
}

function mark_end_to_end_display_time(message_id) {
    if (exports.send_times_data[message_id] === undefined) {
        exports.send_times_data[message_id] = {};
    }
    exports.send_times_data[message_id].displayed = new Date();
    maybe_report_send_times(message_id);
}

exports.mark_rendered_content_disparity = function (message_id, changed) {
    if (exports.send_times_data[message_id] === undefined) {
        exports.send_times_data[message_id] = {};
    }
    exports.send_times_data[message_id].rendered_content_disparity = changed;
};

exports.report_as_received = function report_as_received(message) {
    if (message.sent_by_me) {
        mark_end_to_end_receive_time(message.id);
        setTimeout(function () {
            mark_end_to_end_display_time(message.id);
        }, 0);
    }
};

function process_send_time(message_id, start_time, locally_echoed) {
    var send_finished = new Date();
    var send_time = (send_finished - start_time);
    if (feature_flags.log_send_times) {
        blueslip.log("send time: " + send_time);
    }
    if (feature_flags.collect_send_times) {
        exports.send_times_log.push(send_time);
    }
    if (exports.send_times_data[message_id] === undefined) {
        exports.send_times_data[message_id] = {};
    }
    exports.send_times_data[message_id].start = start_time;
    exports.send_times_data[message_id].send_finished = send_finished;
    exports.send_times_data[message_id].locally_echoed  = locally_echoed;
    maybe_report_send_times(message_id);
}

function clear_compose_box() {
    $("#new_message_content").val('').focus();
    drafts.delete_draft_after_send();
    compose_ui.autosize_textarea();
    $("#send-status").hide(0);
    $("#compose-send-button").removeAttr('disabled');
    $("#sending-indicator").hide();
    resize.resize_bottom_whitespace();
}

exports.send_message_success = function (local_id, message_id, start_time, locally_echoed) {
    if (!locally_echoed) {
        clear_compose_box();
    }

    process_send_time(message_id, start_time, locally_echoed);

    echo.reify_message_id(local_id, message_id);

    setTimeout(function () {
        if (exports.send_times_data[message_id].received === undefined) {
            blueslip.log("Restarting get_events due to delayed receipt of sent message " + message_id);
            server_events.restart_get_events();
        }
    }, 5000);
};

exports.transmit_message = function (request, success, error) {
    delete exports.send_times_data[request.id];
    if (page_params.use_websockets) {
        send_message_socket(request, success, error);
    } else {
        send_message_ajax(request, success, error);
    }
};

function send_message(request) {
    if (request === undefined) {
        request = create_message_object();
    }

    if (request.type === "private") {
        request.to = JSON.stringify(request.to);
    } else {
        request.to = JSON.stringify([request.to]);
    }

    var start_time = new Date();
    var local_id;

    local_id = echo.try_deliver_locally(request);
    if (local_id !== undefined) {
        // We delivered this message locally
        request.local_id = local_id;
    }

    var locally_echoed = local_id !== undefined;

    function success(data) {
        exports.send_message_success(local_id, data.id, start_time, locally_echoed);
    }

    function error(response) {
        // If we're not local echo'ing messages, or if this message was not
        // locally echoed, show error in compose box
        if (request.local_id === undefined) {
            compose_error(response, $('#new_message_content'));
            return;
        }

        echo.message_send_error(local_id, response);
    }

    exports.transmit_message(request, success, error);
    server_events.assert_get_events_running("Restarting get_events because it was not running during send");

    if (locally_echoed) {
        clear_compose_box();
    }
}

exports.enter_with_preview_open = function () {
    exports.clear_preview_area();
    if (page_params.enter_sends) {
        // If enter_sends is enabled, we just send the message
        send_message();
    } else {
        // Otherwise, we return to the compose box and focus it
        $("#new_message_content").focus();
    }
};

// This function is for debugging / data collection only.  Arguably it
// should live in debug.js, but then it wouldn't be able to call
// send_message() directly below.
exports.test_send_many_messages = function (stream, subject, count) {
    var num_sent = 0;

    function do_send_one() {
        var message = {};
        num_sent += 1;

        message.type = "stream";
        message.to = stream;
        message.subject = subject;
        message.content = num_sent.toString();

        send_message(message);

        if (num_sent === count) {
            return;
        }

        setTimeout(do_send_one, 1000);
    }

    do_send_one();
};

exports.finish = function () {
    exports.clear_invites();

    if (! compose.validate()) {
        return false;
    }
    send_message();
    exports.clear_preview_area();
    // TODO: Do we want to fire the event even if the send failed due
    // to a server-side error?
    $(document).trigger($.Event('compose_finished.zulip'));
    return true;
};

$(function () {
    $("#compose form").on("submit", function (e) {
       e.preventDefault();
       compose.finish();
    });
});

exports.update_email = function (user_id, new_email) {
    var reply_to = compose_state.recipient();

    if (!reply_to) {
        return;
    }

    reply_to = people.update_email_in_reply_to(reply_to, user_id, new_email);

    compose_state.recipient(reply_to);
};

exports.get_invalid_recipient_emails = function () {
    var private_recipients = util.extract_pm_recipients(compose_state.recipient());
    var invalid_recipients = [];
    _.each(private_recipients, function (email) {
        // This case occurs when compose_state.recipient() ends with ','
        if (email === "") {
            return;
        }
        if (people.realm_get(email) !== undefined) {
            return;
        }
        if (people.is_cross_realm_email(email)) {
            return;
        }
        invalid_recipients.push(email);
    });

    return invalid_recipients;
};

function check_stream_for_send(stream_name, autosubscribe) {
    var stream_obj = stream_data.get_sub(stream_name);
    var result;
    if (!stream_obj) {
        return "does-not-exist";
    }
    if (stream_obj.subscribed) {
        return "subscribed";
    }
    if (!autosubscribe) {
        return "not-subscribed";
    }

    // In the rare circumstance of the autosubscribe option, we
    // *Synchronously* try to subscribe to the stream before sending
    // the message.  This is deprecated and we hope to remove it; see
    // #4650.
    channel.post({
        url: "/json/subscriptions/exists",
        data: {stream: stream_name, autosubscribe: true},
        async: false,
        success: function (data) {
            if (data.subscribed) {
                result = "subscribed";
            } else {
                result = "not-subscribed";
            }
        },
        error: function (xhr) {
            if (xhr.status === 404) {
                result = "does-not-exist";
            } else {
                result = "error";
            }
        },
    });
    return result;
}

function validate_stream_message_mentions(stream_name) {
    var current_stream = stream_data.get_sub(stream_name);
    var stream_count = current_stream.subscribers.num_items();

    // check if @all or @everyone is in the message
    if (util.is_all_or_everyone_mentioned(compose_state.message_content()) &&
        stream_count > compose.all_everyone_warn_threshold) {
        if (user_acknowledged_all_everyone === undefined ||
            user_acknowledged_all_everyone === false) {
            // user has not seen a warning message yet if undefined
            show_all_everyone_warnings();

            $("#compose-send-button").removeAttr('disabled');
            $("#sending-indicator").hide();
            return false;
        }
    } else {
        // the message no longer contains @all or @everyone
        exports.clear_all_everyone_warnings();
    }
    // at this point, the user has either acknowledged the warning or removed @all / @everyone
    user_acknowledged_all_everyone = undefined;

    return true;
}

function validate_stream_message_address_info(stream_name) {
    var response;

    if (!stream_data.is_subscribed(stream_name)) {
        switch (check_stream_for_send(stream_name, page_params.narrow_stream !== undefined)) {
        case "does-not-exist":
            response = "<p>The stream <b>" +
                Handlebars.Utils.escapeExpression(stream_name) + "</b> does not exist.</p>" +
                "<p>Manage your subscriptions <a href='#streams/all'>on your Streams page</a>.</p>";
            compose_error(response, $('#stream'));
            return false;
        case "error":
            compose_error(i18n.t("Error checking subscription"), $("#stream"));
            return false;
        case "not-subscribed":
            response = "<p>You're not subscribed to the stream <b>" +
                Handlebars.Utils.escapeExpression(stream_name) + "</b>.</p>" +
                "<p>Manage your subscriptions <a href='#streams/all'>on your Streams page</a>.</p>";
            compose_error(response, $('#stream'));
            return false;
        }
    }

    return true;
}

function validate_stream_message() {
    var stream_name = compose_state.stream_name();
    if (stream_name === "") {
        compose_error(i18n.t("Please specify a stream"), $("#stream"));
        return false;
    }

    if (page_params.realm_mandatory_topics) {
        var topic = compose_state.subject();
        if (topic === "") {
            compose_error(i18n.t("Please specify a topic"), $("#subject"));
            return false;
        }
    }

    if (!validate_stream_message_address_info(stream_name) ||
        !validate_stream_message_mentions(stream_name)) {
        return false;
    }

    return true;
}

// The function checks whether the recipients are users of the realm or cross realm users (bots
// for now)
function validate_private_message() {
    if (compose_state.recipient() === "") {
        compose_error(i18n.t("Please specify at least one recipient"), $("#private_message_recipient"));
        return false;
    } else if (page_params.realm_is_zephyr_mirror_realm) {
        // For Zephyr mirroring realms, the frontend doesn't know which users exist
        return true;
    }

    var invalid_recipients = exports.get_invalid_recipient_emails();

    var context = {};
    if (invalid_recipients.length === 1) {
        context = {recipient: invalid_recipients.join()};
        compose_error(i18n.t("The recipient __recipient__ is not valid", context), $("#private_message_recipient"));
        return false;
    } else if (invalid_recipients.length > 1) {
        context = {recipients: invalid_recipients.join()};
        compose_error(i18n.t("The recipients __recipients__ are not valid", context), $("#private_message_recipient"));
        return false;
    }
    return true;
}

exports.validate = function () {
    $("#compose-send-button").attr('disabled', 'disabled').blur();
    $("#sending-indicator").show();

    if (/^\s*$/.test(compose_state.message_content())) {
        compose_error(i18n.t("You have nothing to send!"), $("#new_message_content"));
        return false;
    }

    if ($("#zephyr-mirror-error").is(":visible")) {
        compose_error(i18n.t("You need to be running Zephyr mirroring in order to send messages!"));
        return false;
    }

    if (compose_state.get_message_type() === 'private') {
        return validate_private_message();
    }
    return validate_stream_message();
};

$(function () {
    resize.watch_manual_resize("#new_message_content");

    // Run a feature test and decide whether to display
    // the "Attach files" button
    if (window.XMLHttpRequest && (new XMLHttpRequest()).upload) {
        $("#compose #attach_files").removeClass("notdisplayed");
    }

    // Lazy load the Dropbox script, since it can slow our page load
    // otherwise, and isn't enabled for all users. Also, this Dropbox
    // script isn't under an open source license, so we can't (for legal
    // reasons) minify it with our own code.
    if (feature_flags.dropbox_integration) {
        LazyLoad.js('https://www.dropbox.com/static/api/1/dropins.js', function () {
            // Successful load. We should now have window.Dropbox.
            if (! _.has(window, 'Dropbox')) {
                blueslip.error('Dropbox script reports loading but window.Dropbox undefined');
            } else if (Dropbox.isBrowserSupported()) {
                Dropbox.init({appKey: window.dropboxAppKey});
                $("#compose #attach_dropbox_files").removeClass("notdisplayed");
            }
        });
    }

    // Show a warning if a user @-mentions someone who will not receive this message
    $(document).on('usermention_completed.zulip', function (event, data) {
        if (compose_state.get_message_type() !== 'stream') {
            return;
        }

        // Disable for Zephyr mirroring realms, since we never have subscriber lists there
        if (page_params.realm_is_zephyr_mirror_realm) {
            return;
        }

        if (data !== undefined && data.mentioned !== undefined) {
            var email = data.mentioned.email;

            // warn if @all or @everyone is mentioned
            if (data.mentioned.full_name  === 'all' || data.mentioned.full_name === 'everyone') {
                return; // don't check if @all or @everyone is subscribed to a stream
            }

            if (compose_fade.would_receive_message(email) === false) {
                var new_row = templates.render("compose-invite-users",
                                               {email: email, name: data.mentioned.full_name});
                var error_area = $("#compose_invite_users");

                var existing_invites = _.map($(".compose_invite_user", error_area), function (user_row) {
                    return $(user_row).data('useremail');
                });

                if (existing_invites.indexOf(email) === -1) {
                    error_area.append(new_row);
                }

                error_area.show();
            }
        }

    });

    $("#compose-all-everyone").on('click', '.compose-all-everyone-confirm', function (event) {
        event.preventDefault();

        $(event.target).parents('.compose-all-everyone').remove();
        user_acknowledged_all_everyone = true;
        exports.clear_all_everyone_warnings();
        compose.finish();
    });

    $("#compose_invite_users").on('click', '.compose_invite_link', function (event) {
        event.preventDefault();

        var invite_row = $(event.target).parents('.compose_invite_user');

        var email = $(invite_row).data('useremail');
        if (email === undefined) {
            return;
        }

        function success() {
            var all_invites = $("#compose_invite_users");
            invite_row.remove();

            if (all_invites.children().length === 0) {
                all_invites.hide();
            }
        }

        function failure() {
            var error_msg = invite_row.find('.compose_invite_user_error');
            error_msg.show();

            $(event.target).attr('disabled', true);
        }

        var stream_name = compose_state.stream_name();
        var sub = stream_data.get_sub(stream_name);
        if (!sub) {
            // This should only happen if a stream rename occurs
            // before the user clicks.  We could prevent this by
            // putting a stream id in the link.
            blueslip.warn('Stream no longer exists: ' + stream_name);
            failure();
            return;
        }

        stream_edit.invite_user_to_stream(email, sub, success, failure);
    });

    $("#compose_invite_users").on('click', '.compose_invite_close', function (event) {
        var invite_row = $(event.target).parents('.compose_invite_user');
        var all_invites = $("#compose_invite_users");

        invite_row.remove();

        if (all_invites.children().length === 0) {
            all_invites.hide();
        }
    });

    // Click event binding for "Attach files" button
    // Triggers a click on a hidden file input field

    $("#compose").on("click", "#attach_files", function (e) {
        e.preventDefault();
        $("#compose #file_input").trigger("click");
    } );


    $("#compose").on("click", "#markdown_preview", function (e) {
        e.preventDefault();
        var message = $("#new_message_content").val();
        $("#new_message_content").hide();
        $("#markdown_preview").hide();
        $("#undo_markdown_preview").show();
        $("#preview_message_area").show();

        if (message.length === 0) {
            $("#preview_content").html(i18n.t("Nothing to preview"));
        } else {
            if (markdown.contains_bugdown(message))  {
                var spinner = $("#markdown_preview_spinner").expectOne();
                loading.make_indicator(spinner);
            } else {
                // For messages that don't appear to contain
                // bugdown-specific syntax not present in our
                // marked.js frontend processor, we render using the
                // frontend markdown processor message (but still
                // render server-side to ensure the preview is
                // accurate; if the `markdown.contains_bugdown` logic is
                // incorrect wrong, users will see a brief flicker).
                $("#preview_content").html(markdown.apply_markdown(message));
            }
            channel.post({
                url: '/json/messages/render',
                idempotent: true,
                data: {content: message},
                success: function (response_data) {
                    if (markdown.contains_bugdown(message)) {
                        loading.destroy_indicator($("#markdown_preview_spinner"));
                    }
                    $("#preview_content").html(response_data.rendered);
                },
                error: function () {
                    if (markdown.contains_bugdown(message)) {
                        loading.destroy_indicator($("#markdown_preview_spinner"));
                    }
                    $("#preview_content").html(i18n.t("Failed to generate preview"));
                },
            });
        }
    });

    $("#compose").on("click", "#undo_markdown_preview", function (e) {
        e.preventDefault();
        exports.clear_preview_area();
    });

    $("#compose").on("click", "#attach_dropbox_files", function (e) {
        e.preventDefault();
        var options = {
            // Required. Called when a user selects an item in the Chooser.
            success: function (files) {
                var textbox = $("#new_message_content");
                var links = _.map(files, function (file) { return '[' + file.name + '](' + file.link +')'; })
                             .join(' ') + ' ';
                textbox.val(textbox.val() + links);
            },
            // Optional. A value of false (default) limits selection to a single file, while
            // true enables multiple file selection.
            multiselect: true,
            iframe: true,
        };
        Dropbox.choose(options);
    });

    function uploadStarted() {
        $("#compose-send-button").attr("disabled", "");
        $("#send-status").addClass("alert-info")
                         .show();
        $(".send-status-close").one('click', exports.abort_xhr);
        $("#error-msg").html(
            $("<p>").text(i18n.t("Uploading…"))
                    .after('<div class="progress progress-striped active">' +
                           '<div class="bar" id="upload-bar" style="width: 00%;"></div>' +
                           '</div>'));
    }

    function progressUpdated(i, file, progress) {
        $("#upload-bar").width(progress + "%");
    }

    function uploadError(err, file) {
        var msg;
        $("#send-status").addClass("alert-error")
                        .removeClass("alert-info");
        $("#compose-send-button").removeAttr("disabled");
        switch (err) {
        case 'BrowserNotSupported':
            msg = i18n.t("File upload is not yet available for your browser.");
            break;
        case 'TooManyFiles':
            msg = i18n.t("Unable to upload that many files at once.");
            break;
        case 'FileTooLarge':
            // sanitization not needed as the file name is not potentially parsed as HTML, etc.
            var context = { file_name: file.name };
            msg = i18n.t('"__file_name__" was too large; the maximum file size is 25MiB.', context);
            break;
        case 'REQUEST ENTITY TOO LARGE':
            msg = i18n.t("Sorry, the file was too large.");
            break;
        case 'QuotaExceeded':
            msg = i18n.t("Upload would exceed your maximum quota."
                      + " Consider deleting some previously uploaded files.");
            break;
        default:
            msg = i18n.t("An unknown error occurred.");
            break;
        }
        $("#error-msg").text(msg);
    }

    function uploadFinished(i, file, response) {
        if (response.uri === undefined) {
            return;
        }
        var textbox = $("#new_message_content");
        var split_uri = response.uri.split("/");
        var filename = split_uri[split_uri.length - 1];
        // Urgh, yet another hack to make sure we're "composing"
        // when text gets added into the composebox.
        if (!compose_state.composing()) {
            compose_actions.start('stream');
        }

        var uri = make_upload_absolute(response.uri);

        if (i === -1) {
            // This is a paste, so there's no filename. Show the image directly
            textbox.val(textbox.val() + "[pasted image](" + uri + ") ");
        } else {
            // This is a dropped file, so make the filename a link to the image
            textbox.val(textbox.val() + "[" + filename + "](" + uri + ")" + " ");
        }
        compose_ui.autosize_textarea();
        $("#compose-send-button").removeAttr("disabled");
        $("#send-status").removeClass("alert-info")
                         .hide();

        // In order to upload the same file twice in a row, we need to clear out
        // the #file_input element, so that the next time we use the file dialog,
        // an actual change event is fired.  This is extracted to a function
        // to abstract away some IE hacks.
        clear_out_file_list($("#file_input"));
    }

    // Expose the internal file upload functions to the desktop app,
    // since the linux/windows QtWebkit based apps upload images
    // directly to the server
    if (window.bridge) {
        exports.uploadStarted = uploadStarted;
        exports.progressUpdated = progressUpdated;
        exports.uploadError = uploadError;
        exports.uploadFinished = uploadFinished;
    }

    $("#compose").filedrop({
        url: "/json/upload_file",
        fallback_id: "file_input",
        paramname: "file",
        maxfilesize: page_params.maxfilesize,
        data: {
            // the token isn't automatically included in filedrop's post
            csrfmiddlewaretoken: csrf_token,
        },
        raw_droppable: ['text/uri-list', 'text/plain'],
        drop: uploadStarted,
        progressUpdated: progressUpdated,
        error: uploadError,
        uploadFinished: uploadFinished,
        rawDrop: function (contents) {
            var textbox = $("#new_message_content");
            if (!compose_state.composing()) {
                compose_actions.start('stream');
            }
            textbox.val(textbox.val() + contents);
            compose_ui.autosize_textarea();
        },
    });

    if (page_params.narrow !== undefined) {
        if (page_params.narrow_topic !== undefined) {
            compose_actions.start("stream", {subject: page_params.narrow_topic});
        } else {
            compose_actions.start("stream", {});
        }
    }

    $(document).on('message_id_changed', function (event) {
        if (exports.send_times_data[event.old_id] !== undefined) {
            var value = exports.send_times_data[event.old_id];
            delete exports.send_times_data[event.old_id];
            exports.send_times_data[event.new_id] =
                _.extend({}, exports.send_times_data[event.old_id], value);
        }
    });
});

return exports;
}());

if (typeof module !== 'undefined') {
    module.exports = compose;
}
