# zanaverse_config/brand.py
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
    """
    Must never raise. Wrap in try/except so website pages don't 500.
    """
    try:
        # ensure it's dict-like
        if not isinstance(context, dict):
            return context

        logo  = _logo_url()
        brand = _brand_name()
        context["app_name"]     = brand
        context["brand_html"]   = _brand_html_markup(logo, brand)
        context["logo"]         = logo
        context["favicon"]      = logo
        context["splash_image"] = logo
        context["banner_image"] = logo
    except Exception:
        # absolutely never crash the request
        pass
    return context

# -------------------- app switcher renaming --------------------

APP_TITLE_MAP = {
    "ERPNext":   "ZanaERP",
    "Frappe HR": "ZanaHR",
    "Helpdesk":  "ZanaSupport",
    "Insights":  "Zanalytics",
    "Frappe CRM": "ZanaCRM", # <- new
    "CRM":        "ZanaCRM"  # <- new
}

def _rename_apps_in_bootinfo(bootinfo):
    try:
        installed = bootinfo.get("installed_apps")
        if isinstance(installed, dict):
            for _, meta in installed.items():
                if isinstance(meta, dict):
                    title = meta.get("title")
                    if title in APP_TITLE_MAP:
                        meta["title"] = APP_TITLE_MAP[title]

        apps_list = bootinfo.get("apps") or bootinfo.get("applications") or bootinfo.get("app_list")
        if isinstance(apps_list, list):
            for meta in apps_list:
                if isinstance(meta, dict):
                    title = meta.get("title")
                    if title in APP_TITLE_MAP:
                        meta["title"] = APP_TITLE_MAP[title]
    except Exception:
        # never block boot
        pass

# -------------------- desk boot --------------------

def boot_session(bootinfo):
    """
    Also must never raise.
    """
    brand = _brand_name()
    logo  = _logo_url()

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

    # keep this call *inside* the function
    _rename_apps_in_bootinfo(bootinfo)
    return bootinfo

# -------------------- shims required by hooks --------------------

def app_logo_url():
    # used by hooks.py -> app_logo_url
    return _logo_url()

def brand_html():
    # used by hooks.py -> brand_html
    return _brand_html_markup(_logo_url(), _brand_name())


# -------------------- global email footer enforcement --------------------

ZANAVERSE_FOOTER = "— Sent via Zanaverse ERP"

def _get_current_footer() -> str:
    try:
        return frappe.db.get_single_value("System Settings", "email_footer_address") or ""
    except Exception:
        return ""

def _set_footer(value: str):
    frappe.db.set_single_value("System Settings", "email_footer_address", value)
    frappe.db.commit()

def set_global_footer():
    """One-time set on install (new sites)."""
    try:
        if _get_current_footer() != ZANAVERSE_FOOTER:
            _set_footer(ZANAVERSE_FOOTER)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Zanaverse: set_global_footer failed")

def enforce_global_footer():
    """Self-heal: ensure footer remains Zanaverse (runs after migrate + daily)."""
    try:
        if _get_current_footer() != ZANAVERSE_FOOTER:
            _set_footer(ZANAVERSE_FOOTER)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Zanaverse: enforce_global_footer failed")

# -------------------- CRM branding (translations) --------------------

def _crm_brand_name() -> str:
    # per-site override (optional) -> site_config.json: {"crm_brand_name": "AcmeCRM"}
    try:
        return (frappe.get_site_config() or {}).get("crm_brand_name") or "ZanaCRM"
    except Exception:
        return "ZanaCRM"

def _upsert_translation(src: str, dst: str, lang: str = "en"):
    name = frappe.db.get_value("Translation", {"language": lang, "source_text": src})
    if name:
        doc = frappe.get_doc("Translation", name)
        if doc.translated_text != dst:
            doc.translated_text = dst
            doc.save(ignore_permissions=True)
    else:
        frappe.get_doc({
            "doctype": "Translation",
            "language": lang,
            "source_text": src,
            "translated_text": dst,
        }).insert(ignore_permissions=True)
    frappe.db.commit()

def apply_crm_brand(lang_codes=None):
    """
    Idempotent. Ensures 'Frappe CRM' strings show your brand (default 'ZanaCRM').
    Run on after_migrate and can be run manually on any site.
    """
    langs = lang_codes or ["en", "en-GB"]
    brand = _crm_brand_name()
    strings = {
        "Welcome to Frappe CRM": f"Welcome to {brand}",
        "Frappe CRM": brand,   # catches other spots including tiles/tooltips
    }
    for lang in langs:
        for src, dst in strings.items():
            _upsert_translation(src, dst, lang)
    try:
        frappe.clear_cache()
    except Exception:
        pass
