import frappe

def after_install():
    """Setup default data after app install."""
    create_default_yoga_types()
    frappe.db.commit()

def create_default_yoga_types():
    yoga_types = [
        "Hatha Yoga", "Vinyasa Flow", "Ashtanga", "Kundalini",
        "Yin Yoga", "Restorative Yoga", "Power Yoga", "Prenatal Yoga",
        "Chair Yoga", "Kids Yoga"
    ]
    for yt in yoga_types:
        if not frappe.db.exists("Yoga Type", yt):
            doc = frappe.new_doc("Yoga Type")
            doc.yoga_type_name = yt
            doc.insert(ignore_permissions=True)
