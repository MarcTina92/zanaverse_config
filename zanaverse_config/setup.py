import frappe

def set_default_email_footer():
    """Ensure a global default footer so mails don't show 'Sent via ERPNext'."""
    try:
        frappe.db.set_single_value(
            "System Settings",
            "default_outgoing_footer",
            "— Sent via Zanaverse ERP",
        )
        frappe.clear_cache()
    except Exception:
        frappe.log_error("Failed to set System Settings.default_outgoing_footer",
                         "zanaverse_config: set_default_email_footer")
