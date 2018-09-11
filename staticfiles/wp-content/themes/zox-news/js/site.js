window._wpemojiSettings = {
    "baseUrl": "https:\/\/s.w.org\/images\/core\/emoji\/11\/72x72\/",
    "ext": ".png",
    "svgUrl": "https:\/\/s.w.org\/images\/core\/emoji\/11\/svg\/",
    "svgExt": ".svg",
    "source": {"concatemoji": "http:\/\/www.mvpthemes.com\/zoxnews\/wp-includes\/js\/wp-emoji-release.min.js?ver=4.9.8"}
};
!function (a, b, c) {
    function d(a, b) {
        var c = String.fromCharCode;
        l.clearRect(0, 0, k.width, k.height), l.fillText(c.apply(this, a), 0, 0);
        var d = k.toDataURL();
        l.clearRect(0, 0, k.width, k.height), l.fillText(c.apply(this, b), 0, 0);
        var e = k.toDataURL();
        return d === e
    }

    function e(a) {
        var b;
        if (!l || !l.fillText) return !1;
        switch (l.textBaseline = "top", l.font = "600 32px Arial", a) {
            case"flag":
                return !(b = d([55356, 56826, 55356, 56819], [55356, 56826, 8203, 55356, 56819])) && (b = d([55356, 57332, 56128, 56423, 56128, 56418, 56128, 56421, 56128, 56430, 56128, 56423, 56128, 56447], [55356, 57332, 8203, 56128, 56423, 8203, 56128, 56418, 8203, 56128, 56421, 8203, 56128, 56430, 8203, 56128, 56423, 8203, 56128, 56447]), !b);
            case"emoji":
                return b = d([55358, 56760, 9792, 65039], [55358, 56760, 8203, 9792, 65039]), !b
        }
        return !1
    }

    function f(a) {
        var c = b.createElement("script");
        c.src = a, c.defer = c.type = "text/javascript", b.getElementsByTagName("head")[0].appendChild(c)
    }

    var g, h, i, j, k = b.createElement("canvas"), l = k.getContext && k.getContext("2d");
    for (j = Array("flag", "emoji"), c.supports = {
        everything: !0,
        everythingExceptFlag: !0
    }, i = 0; i < j.length; i++) c.supports[j[i]] = e(j[i]), c.supports.everything = c.supports.everything && c.supports[j[i]], "flag" !== j[i] && (c.supports.everythingExceptFlag = c.supports.everythingExceptFlag && c.supports[j[i]]);
    c.supports.everythingExceptFlag = c.supports.everythingExceptFlag && !c.supports.flag, c.DOMReady = !1, c.readyCallback = function () {
        c.DOMReady = !0
    }, c.supports.everything || (h = function () {
        c.readyCallback()
    }, b.addEventListener ? (b.addEventListener("DOMContentLoaded", h, !1), a.addEventListener("load", h, !1)) : (a.attachEvent("onload", h), b.attachEvent("onreadystatechange", function () {
        "complete" === b.readyState && c.readyCallback()
    })), g = c.source || {}, g.concatemoji ? f(g.concatemoji) : g.wpemoji && g.twemoji && (f(g.twemoji), f(g.wpemoji)))
}(window, document, window._wpemojiSettings);

jQuery(document).ready(function ($) {
    $(window).load(function () {
        var leaderHeight = $("#mvp-leader-wrap").outerHeight();
        var logoHeight = $("#mvp-main-nav-top").outerHeight();
        var botHeight = $("#mvp-main-nav-bot").outerHeight();
        var navHeight = $("#mvp-main-head-wrap").outerHeight();
        var headerHeight = navHeight + leaderHeight;
        var aboveNav = leaderHeight + logoHeight;
        var totalHeight = logoHeight + botHeight;
        var previousScroll = 0;
        $(window).scroll(function (event) {
            var scroll = $(this).scrollTop();
            if ($(window).scrollTop() > aboveNav) {
                $("#mvp-main-nav-top").addClass("mvp-nav-small");
                $("#mvp-main-nav-bot").css("margin-top", logoHeight);
            } else {
                $("#mvp-main-nav-top").removeClass("mvp-nav-small");
                $("#mvp-main-nav-bot").css("margin-top", "0");
            }
            if ($(window).scrollTop() > headerHeight) {
                $("#mvp-main-nav-top").addClass("mvp-fixed");
                $("#mvp-main-nav-bot").addClass("mvp-fixed1");
                $("#mvp-main-body-wrap").css("margin-top", 0);
                $("#mvp-main-nav-top").addClass("mvp-fixed-shadow");
                $(".mvp-fly-top").addClass("mvp-to-top");
                if (scroll < previousScroll) {
                    $("#mvp-main-nav-bot").addClass("mvp-fixed2");
                    $("#mvp-main-nav-top").removeClass("mvp-fixed-shadow");
                } else {
                    $("#mvp-main-nav-bot").removeClass("mvp-fixed2");
                    $("#mvp-main-nav-top").addClass("mvp-fixed-shadow");
                }
            } else {
                $("#mvp-main-nav-top").removeClass("mvp-fixed");
                $("#mvp-main-nav-bot").removeClass("mvp-fixed1");
                $("#mvp-main-nav-bot").removeClass("mvp-fixed2");
                $("#mvp-main-body-wrap").css("margin-top", "0");
                $("#mvp-main-nav-top").removeClass("mvp-fixed-shadow");
                $(".mvp-fly-top").removeClass("mvp-to-top");
            }
            previousScroll = scroll;
        });
    });
});


jQuery(document).ready(function ($) {
    // Mobile Social Buttons More
    $(window).load(function () {
        $(".mvp-soc-mob-right").on("click", function () {
            $("#mvp-soc-mob-wrap").toggleClass("mvp-soc-mob-more");
        });
    });
});


jQuery(document).ready(function ($) {
    // Continue Reading Button
    $(window).load(function () {
        $(".mvp-cont-read-but").on("click", function () {
            $("#mvp-content-body-top").css("max-height", "none");
            $("#mvp-content-body-top").css("overflow", "visible");
            $(".mvp-cont-read-but-wrap").hide();
        });
    });
});


jQuery(document).ready(function ($) {
    $(window).load(function () {
        var leaderHeight = $("#mvp-leader-wrap").outerHeight();
        $("#mvp-site-main").css("margin-top", leaderHeight - 50);
    });

    $(window).resize(function () {
        var leaderHeight = $("#mvp-leader-wrap").outerHeight();
        $("#mvp-site-main").css("margin-top", leaderHeight - 50);
    });

});


jQuery(document).ready(function ($) {
    $(".menu-item-has-children a").click(function (event) {
        event.stopPropagation();

    });

    $(".menu-item-has-children").click(function () {
        $(this).addClass("toggled");
        if ($(".menu-item-has-children").hasClass("toggled")) {
            $(this).children("ul").toggle();
            $(".mvp-fly-nav-menu").getNiceScroll().resize();
        }
        $(this).toggleClass("tog-minus");
        return false;
    });

    // Main Menu Scroll
    $(window).load(function () {
        $(".mvp-fly-nav-menu").niceScroll({cursorcolor: "#888", cursorwidth: 7, cursorborder: 0, zindex: 999999});
    });
});


jQuery(document).ready(function ($) {
    $(".infinite-content").infinitescroll({
        navSelector: ".mvp-nav-links",
        nextSelector: ".mvp-nav-links a:first",
        itemSelector: ".infinite-post",
        errorCallback: function () {
            $(".mvp-inf-more-but").css("display", "none")
        }
    });
    $(window).unbind(".infscr");
    $(".mvp-inf-more-but").click(function () {
        $(".infinite-content").infinitescroll("retrieve");
        return false;
    });
    $(window).load(function () {
        if ($(".mvp-nav-links a").length) {
            $(".mvp-inf-more-but").css("display", "inline-block");
        } else {
            $(".mvp-inf-more-but").css("display", "none");
        }
    });
});