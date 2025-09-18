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
    return (ws and (ws.app_name or ws.brand_html)) or BRAND_NAME

def _logo_url():
    ws = _ws()
    return (ws and (ws.app_logo or ws.splash_image or ws.favicon)) or DEFAULT_LOGO

def _brand_html_markup(logo: str, brand: str) -> str:
    return f'<img src="{logo}" alt="{brand}" style="height:22px;vertical-align:middle">'

# -------------------- website context --------------------

def update_website_context(context):
    logo  = _logo_url()
    brand = _brand_name()
    context["app_name"]     = brand
    context["brand_html"]   = _brand_html_markup(logo, brand)
    context["logo"]         = logo
    context["favicon"]      = logo
    context["splash_image"] = logo
    context["banner_image"] = logo
    return context

def app_logo_url():
    return _logo_url()

def brand_html():
    brand = _brand_name()
    logo  = _logo_url()
    return _brand_html_markup(logo, brand)

# -------------------- app switcher renaming --------------------

APP_TITLE_MAP = {
    "ERPNext":   "ZanaERP",
    "Frappe HR": "ZanaHR",
    "Helpdesk":  "ZanaSupport",
    "Insights":  "Zanalytics",
}

def _rename_apps_in_bootinfo(bootinfo):
    """
    Rename app titles for the /apps switcher across common boot payload layouts.
    Safe to run on any build.
    """
    try:
        # Case A: dict {"erpnext": {"title": "ERPNext", ...}}
        installed = bootinfo.get("installed_apps")
        if isinstance(installed, dict):
            for _, meta in installed.items():
                if not isinstance(meta, dict):
                    continue
                title = meta.get("title")
                if title in APP_TITLE_MAP:
                    meta["title"] = APP_TITLE_MAP[title]

        # Case B: list [{"name":"erpnext","title":"ERPNext"}, ...]
        apps_list = bootinfo.get("apps") or bootinfo.get("applications") or bootinfo.get("app_list")
        if isinstance(apps_list, list):
            for meta in apps_list:
                if not isinstance(meta, dict):
                    continue
                title = meta.get("title")
                if title in APP_TITLE_MAP:
                    meta["title"] = APP_TITLE_MAP[title]
    except Exception:
        # never block boot
        pass

# -------------------- desk boot --------------------

def boot_session(bootinfo):
    brand = _brand_name()
    logo  = _logo_url()

    # Primary fields used by Desk header + titlebar
    try: bootinfo.app_name = brand
    except Exception: pass
    try: bootinfo.brand_html = _brand_html_markup(logo, brand)
    except Exception: pass
    try: bootinfo.app_logo_url = logo
    except Exception: pass
    try: bootinfo.app_logo = logo
    except Exception: pass
    try: bootinfo.favicon = logo
    except Exception: pass
    try: bootinfo.splash_image = logo
    except Exception: pass
    try: bootinfo.sitename = brand
    except Exception: pass

    # Tidy navbar help links if present
    try:
        ns = (bootinfo.get("navbar_settings") or {})
        for k in ("help_menu", "docs_url", "developer_mode"):
            if k in ns:
                ns[k] = [] if isinstance(ns[k], list) else None
        bootinfo["navbar_settings"] = ns
    except Exception:
        pass

    # <<< important: this call must be INSIDE the function body, indented >>>
    _rename_apps_in_bootinfo(bootinfo)

    return bootinfo
