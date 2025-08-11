# zanaverse_config/zanaverse_config/install.py
import frappe

def _safe_set_portal_defaults():
    try:
        ps = frappe.get_doc("Portal Settings", "Portal Settings")
        # only set if empty AND the role actually exists
        if not ps.default_role and frappe.db.exists("Role", "Website User"):
            ps.default_role = "Website User"
            ps.save()
            frappe.db.commit()
    except Exception:
        frappe.db.rollback()

def after_install():
    _safe_set_portal_defaults()

def after_migrate():
    _safe_set_portal_defaults()
