import frappe

BRAND_NAME   = "Zanaverse"
DEFAULT_LOGO = "/assets/zanaverse_config/images/zv-logo.png?v=2"


# -------------------- helpers --------------------

def _ws():
    try:
        return frappe.get_cached_doc("Website Settings", "Website Settings")
    except Exception:
        return None


def _brand_name():
    ws = _ws()
    # prefer explicit Website Settings values; fall back to constant
    return (ws and (ws.app_name or ws.brand_html)) or BRAND_NAME


def _logo_url():
    ws = _ws()
    # prefer app_logo, then splash, then favicon, then default
    return (ws and (ws.app_logo or ws.splash_image or ws.favicon)) or DEFAULT_LOGO


def _brand_html_markup(logo: str, brand: str) -> str:
    return f'<img src="{logo}" alt="{brand}" style="height:22px;vertical-align:middle">'


# -------------------- hook implementations --------------------

def update_website_context(context):
    """
    Ensure website templates (login, reset, error, public pages) receive consistent branding.
    """
    logo  = _logo_url()
    brand = _brand_name()

    # Common keys used across Website / Navbar / Jinja templates
    context["app_name"]     = brand
    context["brand_html"]   = _brand_html_markup(logo, brand)
    context["logo"]         = logo
    context["favicon"]      = logo
    context["splash_image"] = logo
    context["banner_image"] = logo
    return context


def app_logo_url():
    """Logo shown in the Desk navbar (top-left)."""
    return _logo_url()


def brand_html():
    """Inline brand markup fallback consumed by Desk header."""
    brand = _brand_name()
    logo  = _logo_url()
    return _brand_html_markup(logo, brand)


def boot_session(bootinfo):
    """
    Runs during Desk boot. Set authoritative values so Setup Wizard + SPA
    render Zanaverse branding without client hacks.
    """
    brand = _brand_name()
    logo  = _logo_url()

    # Primary fields used by Desk header + titlebar
    try: bootinfo.app_name = brand
    except Exception: pass

    # Some builds look for brand_html as *text*; others accept markup.
    # Provide both, plus app_logo_url/app_logo for wide compatibility.
    try: bootinfo.brand_html = _brand_html_markup(logo, brand)  # safe text
    except Exception: pass
    try: bootinfo.app_logo_url = logo
    except Exception: pass
    try: bootinfo.app_logo = logo
    except Exception: pass

    # Favicon + splash in boot payload (some themes read these)
    try: bootinfo.favicon = logo
    except Exception: pass
    try: bootinfo.splash_image = logo
    except Exception: pass

    # Site title hint (affects document.title in some builds)
    try: bootinfo.sitename = brand
    except Exception: pass

    # Tidy/neutralise help/support links if present in navbar_settings
    try:
        ns = (bootinfo.get("navbar_settings") or {})
        # Nuke/blank common keys we don't want pointing to external docs
        for k in ("help_menu", "docs_url", "developer_mode"):
            if k in ns:
                ns[k] = [] if isinstance(ns[k], list) else None
        bootinfo["navbar_settings"] = ns
    except Exception:
        pass

    return bootinfo
