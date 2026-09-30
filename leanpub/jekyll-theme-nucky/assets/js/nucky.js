/* ===========================================================================
 * nucky.js – skripty temy jekyll-theme-nucky
 *
 * Nacitava sa blokujuco v <head> (BEZ defer/async), aby sa farebny rezim
 * nastavil este pred vykreslenim stranky a nedoslo k bliknutiu.
 * =========================================================================== */

(function () {
    "use strict";

    /* -----------------------------------------------------------------------
     * Farebny rezim (svetly / tmavy / podla systemu)
     * Bezi okamzite – nastavi <html data-bs-theme> a spravnu temu pre
     * highlight.js este pocas parsovania <head>.
     * --------------------------------------------------------------------- */
    var mediaDark = window.matchMedia("(prefers-color-scheme: dark)");

    function resolveMode(choice) {
        if (choice === "light" || choice === "dark") return choice;
        return mediaDark.matches ? "dark" : "light";
    }

    function applyMode(mode) {
        document.documentElement.setAttribute("data-bs-theme", mode);

        var lightCss = document.getElementById("hljs-light");
        var darkCss = document.getElementById("hljs-dark");
        if (lightCss && darkCss) {
            lightCss.disabled = mode === "dark";
            darkCss.disabled = mode !== "dark";
        }
    }

    window.getStoredTheme = function () {
        try {
            return localStorage.getItem("theme") || "auto";
        } catch (e) {
            return "auto";
        }
    };

    window.setTheme = function (choice) {
        try {
            if (choice === "light" || choice === "dark") localStorage.setItem("theme", choice);
            else localStorage.removeItem("theme");
        } catch (e) { /* localStorage nedostupny – pokracuj bez ulozenia */ }
        applyMode(resolveMode(choice));
    };

    // pociatocne nastavenie
    (function () {
        var stored = null;
        try { stored = localStorage.getItem("theme"); } catch (e) { /* ignoruj */ }
        applyMode(resolveMode(stored));
    })();


    /* -----------------------------------------------------------------------
     * Zvysok – az ked je DOM pripraveny
     * --------------------------------------------------------------------- */
    document.addEventListener("DOMContentLoaded", function () {

        // Zvyraznenie syntaxe (highlight.min.js sa nacita pred DOMContentLoaded)
        if (window.hljs) window.hljs.highlightAll();

        // Bootstrap styl pre tabulky z Markdownu
        // (obrazky su responzivne cez CSS – #wrap img v custom.css)
        document.querySelectorAll("table").forEach(function (el) {
            el.classList.add("table", "table-striped");
        });

        // Prepinac farebneho rezimu v navigacii
        var current = window.getStoredTheme();
        var buttons = document.querySelectorAll("[data-bs-theme-value]");
        var themeIcon = document.getElementById("theme-icon");
        var glyphs = { light: "fa-sun", dark: "fa-moon", auto: "fa-adjust" };

        function markActive(value) {
            buttons.forEach(function (b) {
                b.classList.toggle("active", b.getAttribute("data-bs-theme-value") === value);
            });
            if (themeIcon) {
                themeIcon.classList.remove("fa-sun", "fa-moon", "fa-adjust");
                themeIcon.classList.add(glyphs[value] || "fa-adjust");
            }
        }

        markActive(current);
        buttons.forEach(function (btn) {
            btn.addEventListener("click", function () {
                var value = btn.getAttribute("data-bs-theme-value");
                window.setTheme(value);
                markActive(value);
            });
        });

        // Pri rezime "auto" reaguj na zmenu systemoveho nastavenia
        mediaDark.addEventListener("change", function () {
            if (window.getStoredTheme() === "auto") window.setTheme("auto");
        });
    });
})();
