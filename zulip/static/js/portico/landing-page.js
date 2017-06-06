// this will either smooth scroll to an anchor where the `name`
// is the same as the `scroll-to` reference, or to a px height
// (as specified like `scroll-to='0px'`).
var ScrollTo = function () {
    $("[scroll-to]").click(function () {
        var sel = $(this).attr("scroll-to");

        // if the `scroll-to` is a parse-able pixel value like `50px`,
        // then use that as the scrollTop, else assume it is a selector name
        // and find the `offsetTop`.
        var top = /\dpx/.test(sel) ?
                parseInt(sel, 10) :
                $("[name='" + sel + "']").offset().top;

        $("body").animate({ scrollTop: top + "px" }, 300);
    });
};

// these are events that are only to run on the integrations page.
// check if the page location is integrations.
var integration_events = function () {
    var scroll_top = 0;

    $("a.title")
        .addClass("show-integral")
        .prepend($("<span class='integral'>∫</span>"))
        .hover(function () {
            $(".integral").css("display", "inline");
            var width = $(".integral").width();
            $("a.title").css("left", -1 * width);
        },
        function () {
            $(".integral").css("display", "none");
                $("a.title").css("left", 0);
            }
        );

    var $lozenge_icon;
    var currentblock;
    var instructionbox = $("#integration-instruction-block");
    var hashes = $('.integration-instructions').map(function () {
        return this.id || null;
    }).get();


    var show_integration = function (hash) {
        // the version of the hash without the leading "#".
        var _hash = hash.replace(/^#/, "");

        // clear out the integrations instructions that may exist in the instruction
        // block from a previous hash.
        $("#integration-instruction-block .integration-instructions")
            .appendTo("#integration-instructions-group");

        if (hashes.indexOf(_hash) > -1) {
            $lozenge_icon = $(".integration-lozenges .integration-lozenge.integration-" + _hash).clone(true);
            currentblock = $(hash);
            instructionbox.hide().children(".integration-lozenge").replaceWith($lozenge_icon);
            instructionbox.append($lozenge_icon);

            $(".inner-content").removeClass("show");
            setTimeout(function () {
                instructionbox.hide();
                $(".integration-lozenges").addClass("hide");
                $(".extra, #integration-main-text").hide();

                instructionbox.append(currentblock);
                instructionbox.show();
                $("#integration-list-link").css("display", "block");

                $(".inner-content").addClass("show");
            }, 300);

            $("html, body").animate({ scrollTop: 0 }, 200);
        }
    };

    function update_hash() {
        var hash = window.location.hash;

        if (hash && hash !== '#hubot-integrations') {
            scroll_top = $("body").scrollTop();
            show_integration(window.location.hash);
        } else if (currentblock && $lozenge_icon) {
            $(".inner-content").removeClass("show");
            setTimeout(function () {
                $("#integration-list-link").css("display", "none");
                $(".integration-lozenges").removeClass("hide");
                $(".extra, #integration-main-text").show();
                instructionbox.hide();
                $lozenge_icon.remove();
                currentblock.appendTo("#integration-instructions-group");
                $(".inner-content").addClass("show");

                $('html, body').animate({ scrollTop: scroll_top }, 0);
            }, 300);
        } else {
            $(".inner-content").addClass("show");
        }
    }

    window.onhashchange = update_hash;
    update_hash();

    // this needs to happen because when you link to "#" it will scroll to the
    // top of the page.
    $("#integration-list-link").click(function (e) {
        var scroll_height = $("body").scrollTop();
        window.location.hash = "#";
        $("body").scrollTop(scroll_height);

        e.preventDefault();
    });
};

var hello_events = function () {
    var counter = 0;
    $(window).scroll(function () {
        if (counter % 2 === 0) {
            $(".screen.hero-screen .message-feed").css("transform", "translateY(-" + $(this).scrollTop() / 5 + "px)");
        }
        counter += 1;
    });

    $(".footer").addClass("hello");
};

var events = function () {
    ScrollTo();

    $("a").click(function (e) {
        // if the pathname is different than what we are already on, run the
        // custom transition function.
        if (window.location.pathname !== this.pathname && !this.hasAttribute("download")) {
            e.preventDefault();
            $(".portico-landing").removeClass("show");
            setTimeout(function () {
                window.location.href = $(this).attr("href");
            }.bind(this), 500);
        }
    });

    // get the location url like `zulipchat.com/features/`, cut off the trailing
    // `/` and then split by `/` to get ["zulipchat.com", "features"], then
    // pop the last element to get the current section (eg. `features`).
    var location = window.location.pathname.replace(/\/#*$/, "").split(/\//).pop();

    $("[on-page='" + location + "']").addClass("active");

    $("body").click(function (e) {
        var $e = $(e.target);

        var should_close = !$e.is("ul, .hamburger") && $e.closest("ul, .hamburger").length === 0;

        // this means that it is in mobile sidebar mode.
        if ($("nav ul").height() === window.innerHeight && should_close) {
            $("nav ul").removeClass("show");
        }
    });

    $(".hamburger").click(function () {
        $("nav ul").addClass("show");
    });

    (function () {
        var $last = $(".details-box").eq(0).addClass("show");
        var $li = $("ul.sidebar li");
        var version;

        var nav_version = {
            Win: "windows",
            MacIntel: "mac",
            Linux: "linux",
            iP: "ios",
        };

        for (var x in nav_version) {
            if (navigator.platform.indexOf(x) !== -1) {
                $('li[data-name="' + nav_version[x] + '"]').click();
                version = nav_version[x];
                break;
            }
        }

        var switch_to_tab = function (elem) {
            var target = $(elem).data("name");
            var $el = $(".details-box[data-name='" + target + "']");

            // $li is a semi-global variable from the closure above.
            $li.removeClass("active");
            $(elem).addClass("active");

            $last.removeClass("show");
            $el.addClass("show");

            $last = $el;
        };

        // this is for the sidebar on the /apps/ page to trigger the correct info box.
        $li.click(function () {
            window.location.hash = $(this).data("name");
        });

        if (window.location.pathname === "/apps/") {
            var hash = function () {
                return window.location.hash.replace(/^#/, "");
            };

            switch_to_tab($("ul.sidebar li[data-name='" + (hash() || version || "windows") + "']"));

            window.onhashchange = function () {
                switch_to_tab($("ul.sidebar li[data-name='" + hash() + "']"));
            };
        }
    }());

    if (/\/integrations\/*/.test(window.location.pathname)) {
        integration_events();
    }

    if (/\/hello\/*/.test(window.location.pathname)) {
        hello_events();
    }
};

// run this callback when the page is determined to have loaded.
var load = function () {
    // show the .portico-landing when the document is loaded.
    setTimeout(function () {
        $(".portico-landing").addClass("show");
    }, 200);

    // display the `x-grad` element a second after load so that the slide up
    // transition on the .portico-landing is nice and smooth.
    setTimeout(function () {
        $("x-grad").addClass("show");
    }, 1000);

    // Set events.
    events();
};

if (document.readyState === "complete") {
    load();
} else {
    $(document).ready(load);
}
