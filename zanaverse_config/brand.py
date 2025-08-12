import frappe

# One stable fallback inside your app (matches what you just set)
DEFAULT_LOGO = "/assets/zanaverse_config/images/zv-logo.png?v=2"

def _ws():
    try:
        return frappe.get_cached_doc("Website Settings", "Website Settings")
    except Exception:
        return None

def _current_logo():
    ws = _ws()
    return (ws and (ws.app_logo or ws.splash_image or ws.favicon)) or DEFAULT_LOGO

# ---- Hooks ----
def update_website_context(context):
    """
    Ensures all website templates (login, update-password, message, error, etc.)
    receive the same logo + favicon.
    """
    logo = _current_logo()
    context["logo"] = logo
    context["favicon"] = logo
    # optional extras if you want:
    context["splash_image"] = logo
    context["banner_image"] = logo

def app_logo_url():
    """Desk (top-left) logo at boot."""
    return _current_logo()

def brand_html():
    """Fallback HTML for places that render inline brand markup."""
    ws = _ws()
    app = (ws and ws.app_name) or "Zanaverse"
    logo = _current_logo()
    return f'<img src="{logo}" alt="{app}" style="height:22px;vertical-align:middle">'
