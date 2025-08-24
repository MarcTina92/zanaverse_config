import frappe

BRAND_NAME   = "Zanaverse"
# keep your existing asset path
DEFAULT_LOGO = "/assets/zanaverse_config/images/zv-logo.png?v=2"


def _ws():
    try:
        return frappe.get_cached_doc("Website Settings", "Website Settings")
    except Exception:
        return None


def _brand_name():
    ws = _ws()
    return (ws and (ws.app_name or ws.brand_html)) or BRAND_NAME


def _logo_url():
    ws = _ws()
    # prefer explicit app_logo, then splash, then favicon, then default
    return (ws and (ws.app_logo or ws.splash_image or ws.favicon)) or DEFAULT_LOGO


# -------------------- hooks --------------------

def update_website_context(context):
    """
    Ensures website templates (login, update-password, message, error, etc.)
    receive consistent branding.
    """
    logo = _logo_url()
    brand = _brand_name()

    # Common keys used by Website / Navbar / templates
    context["app_name"] = brand
    context["brand_html"] = f'<img src="{logo}" alt="{brand}" style="height:22px;vertical-align:middle">'
    context["logo"]         = logo
    context["favicon"]      = logo
    context["splash_image"] = logo
    context["banner_image"] = logo


def app_logo_url():
    """Logo shown in the Desk navbar (top-left)."""
    return _logo_url()


def brand_html():
    """Inline brand markup fallback (OK to keep your <img>-based variant)."""
    brand = _brand_name()
    logo  = _logo_url()
    return f'<img src="{logo}" alt="{brand}" style="height:22px;vertical-align:middle">'


def boot_session(bootinfo):
    """
    Runs during Desk boot. Set authoritative values here so the SPA (incl. Setup Wizard)
    uses 'Zanaverse' everywhere without needing client-side hacks.
    """
    brand = _brand_name()
    logo  = _logo_url()

    bootinfo.app_name   = brand          # drives document.title + navbar
    bootinfo.brand_html = brand          # additional consumers
    # harmless extras some themes consume:
    bootinfo.app_logo   = logo
    bootinfo.favicon    = logo
    return bootinfo
