var settings_streams = (function () {

var exports = {};

var meta = {
    loaded: false,
};

exports.reset = function () {
    meta.loaded = false;
};

var all_streams = [];

function failed_listing_streams(xhr) {
    ui_report.error(i18n.t("Error listing streams"), xhr, $("#organization-status"));
}

function populate_streams(streams_data) {
    var streams_table = $("#admin_streams_table").expectOne();
    all_streams = streams_data;

    list_render(streams_table, all_streams.streams, {
        name: "admin_streams_list",
        modifier: function (item) {
            return templates.render("admin_streams_list", { stream: item });
        },
        filter: {
            element: streams_table.closest(".settings-section").find(".search"),
            callback: function (item, value) {
                return item.name.toLowerCase().match(value);
            },
        },
    }).init();

    loading.destroy_indicator($('#admin_page_streams_loading_indicator'));
}

exports.build_default_stream_table = function (streams_data) {
    var self = {};

    self.row_dict = new Dict();

    var table = $("#admin_default_streams_table").expectOne();

    list_render(table, streams_data, {
        name: "default_streams_list",
        modifier: function (item) {
            var row = $(templates.render("admin_default_streams_list", { stream: item, can_modify: page_params.is_admin }));
            self.row_dict.set(item.stream_id, row);
            return row;
        },
        filter: {
            element: table.closest(".settings-section").find(".search"),
            callback: function (item, value) {
                return item.name.toLowerCase().match(value);
            },
        },
    }).init();

    loading.destroy_indicator($('#admin_page_default_streams_loading_indicator'));

    self.remove = function (stream_id) {
        if (self.row_dict.has(stream_id)) {
            var row = self.row_dict.get(stream_id);
            row.remove();
        }
    };

    return self;
};

var default_stream_table;

exports.remove_default_stream = function (stream_id) {
    if (default_stream_table) {
        default_stream_table.remove(stream_id);
    }
};

function get_non_default_streams_names(streams_data) {
    var non_default_streams_names = [];
    var default_streams_names = [];

    _.each(page_params.realm_default_streams, function (default_stream) {
        default_streams_names.push(default_stream.name);
    });

    _.each(streams_data.streams, function (stream) {
        if (default_streams_names.indexOf(stream.name) < 0) {
            non_default_streams_names.push(stream.name);
        }
    });
    return non_default_streams_names;
}

exports.update_default_streams_table = function () {
    if (/#*organization/.test(window.location.hash) ||
        /#*settings/.test(window.location.hash)) {
        $("#admin_default_streams_table").expectOne().find("tr.default_stream_row").remove();
        default_stream_table = exports.build_default_stream_table(
            page_params.realm_default_streams);
    }
};

function make_stream_default(stream_name) {
    var data = {
        stream_name: stream_name,
    };
    var default_stream_status = $("#admin-default-stream-status");
    default_stream_status.hide();

    channel.post({
        url: '/json/default_streams',
        data: data,
        error: function (xhr) {
            if (xhr.status.toString().charAt(0) === "4") {
                ui_report.error(i18n.t("Failed"), xhr, default_stream_status);
            } else {
                ui_report.error(i18n.t("Failed"), default_stream_status);
            }
            default_stream_status.show();
        },
    });
}

exports.set_up = function () {
    loading.make_indicator($('#admin_page_streams_loading_indicator'));

    // Populate streams table
    channel.get({
        url:      '/json/streams?include_public=true&include_subscribed=true&include_default=true',
        timeout:  10*1000,
        idempotent: true,
        success: exports.on_load_success,
        error: failed_listing_streams,
    });
};

exports.on_load_success = function (streams_data) {
    meta.loaded = true;

    populate_streams(streams_data);

    exports.update_default_streams_table();

    $(".admin_stream_table").on("click", ".deactivate", function (e) {
        e.preventDefault();
        e.stopPropagation();

        $(".active_stream_row").removeClass("active_stream_row");
        var row = $(e.target).closest(".stream_row");
        row.addClass("active_stream_row");

        var stream_name = row.find('.stream_name').text();

        $("#deactivation_stream_modal .stream_name").text(stream_name);
        $("#deactivation_stream_modal").modal("show");
    });

    $('.create_default_stream').keypress(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            e.stopPropagation();
            var default_stream_input = $(".create_default_stream");
            make_stream_default(default_stream_input.val());
            default_stream_input[0].value = "";
        }
    });

    $('.create_default_stream').typeahead({
        items: 5,
        fixed: true,
        source: function () {
            return get_non_default_streams_names(all_streams);
        },
        highlight: true,
        updater: function (stream_name) {
            make_stream_default(stream_name);
        },
    });

    $(".default-stream-form").on("click", "#do_submit_stream", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var default_stream_input = $(".create_default_stream");
        make_stream_default(default_stream_input.val());
        // Clear value inside input box
        default_stream_input[0].value = "";
    });

    $("#do_deactivate_stream_button").click(function () {
        if ($("#deactivation_stream_modal .stream_name").text() !== $(".active_stream_row").find('.stream_name').text()) {
            blueslip.error("Stream deactivation canceled due to non-matching fields.");
            ui_report.message("Deactivation encountered an error. Please reload and try again.",
               $("#home-error"), 'alert-error');
        }
        $("#deactivation_stream_modal").modal("hide");
        $(".active_stream_row button").prop("disabled", true).text(i18n.t("Working…"));
        var stream_name = $(".active_stream_row").find('.stream_name').text();
        var stream_id = stream_data.get_sub(stream_name).stream_id;
        channel.del({
            url: '/json/streams/' + stream_id,
            error: function (xhr) {
                if (xhr.status.toString().charAt(0) === "4") {
                    $(".active_stream_row button").closest("td").html(
                        $("<p>").addClass("text-error").text(JSON.parse(xhr.responseText).msg)
                    );
                } else {
                    $(".active_stream_row button").text(i18n.t("Failed!"));
                }
            },
            success: function () {
                var row = $(".active_stream_row");
                row.remove();
            },
        });
    });

};

return exports;
}());

if (typeof module !== 'undefined') {
    module.exports = settings_streams;
}
