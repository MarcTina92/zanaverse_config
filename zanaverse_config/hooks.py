# ~/frappe-bench/apps/zanaverse_config/zanaverse_config/hooks.py

app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"


# Desk brand (top-left)
app_logo_url = "/assets/zanaverse_config/images/logo.svg?v=2"
brand_html = '<img src="/assets/zanaverse_config/images/logo.svg?v=2" alt="Zanaverse" style="height:22px;vertical-align:middle">'

# Load our CSS early so it catches the preloader
app_include_css = "/assets/zanaverse_config/css/brand.css"

# (Optional) Preload the logo so it’s ready immediately
app_include_head = ['<link rel="preload" as="image" href="/assets/zanaverse_config/images/logo.svg?v=2">']


# Keep fixtures minimal (only what you truly need)
fixtures = [
    {"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]},
]

# Desk brand (top-left) – used at boot
app_logo_url = "/assets/zanaverse_config/images/logo.svg?v=1"

# Optional fallback brand HTML (Desk header, where applicable)
brand_html = '<img src="/assets/zanaverse_config/images/logo.svg?v=1" alt="Zanaverse" style="height:22px;vertical-align:middle">'

# Force the Desk preloader to use our logo (belt & braces: preload + CSS + JS)
app_include_head = [
    '<link rel="preload" as="image" href="/assets/zanaverse_config/images/logo.svg?v=1">',

    """
    <style>
      /* Use our logo as a pseudo-element on splash to avoid any default flash */
      .splash::before {
        content: "";
        display: block;
        width: 64px;
        height: 64px;
        margin: 0 auto;
        background: url('/assets/zanaverse_config/images/logo.svg?v=1') center/contain no-repeat;
      }
      /* Hide whatever built-in image Frappe tries to show */
      .splash img,
      .splash .logo img,
      img.app-logo {
        opacity: 0 !important;
      }
    </style>
    """,

    """
    <script>
      (function () {
        var WANT = "/assets/zanaverse_config/images/logo.svg?v=1";
        function swapOnce() {
          var el = document.querySelector(".splash img, .splash .logo img, img.app-logo");
          if (el && (!el.src || !el.src.includes("zanaverse_config"))) {
            el.src = WANT;
          }
        }
        // try immediately, then for a short period during boot
        swapOnce();
        var t0 = Date.now();
        var iv = setInterval(function () {
          swapOnce();
          if (Date.now() - t0 > 3000) clearInterval(iv);
        }, 50);
        window.addEventListener("load", function () {
          setTimeout(swapOnce, 0);
        });
      })();
    </script>
    """,
]

# Branding hooks
after_install = "zanaverse_config.install.apply_branding_first_time"
after_migrate = "zanaverse_config.install.apply_branding"
