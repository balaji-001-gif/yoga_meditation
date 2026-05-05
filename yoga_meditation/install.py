import frappe

def after_install():
    """Setup default data after app install."""
    create_default_yoga_types()
    create_default_meditation_types()
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

def create_default_meditation_types():
    med_types = [
        "Mindfulness Meditation", "Guided Visualization", "Breathwork (Pranayama)",
        "Body Scan", "Loving Kindness (Metta)", "Transcendental Meditation",
        "Chakra Meditation", "Sound Bath", "Walking Meditation"
    ]
    for mt in med_types:
        if not frappe.db.exists("Meditation Type", mt):
            doc = frappe.new_doc("Meditation Type")
            doc.meditation_type_name = mt
            doc.insert(ignore_permissions=True)
