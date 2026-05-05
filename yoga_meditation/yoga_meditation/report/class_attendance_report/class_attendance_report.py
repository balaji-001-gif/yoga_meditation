import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Date"), "fieldname": "class_date", "fieldtype": "Date", "width": 100},
        {"label": _("Class"), "fieldname": "class_name", "fieldtype": "Data", "width": 180},
        {"label": _("Type"), "fieldname": "class_type", "fieldtype": "Data", "width": 100},
        {"label": _("Instructor"), "fieldname": "instructor", "fieldtype": "Link", "options": "Instructor", "width": 130},
        {"label": _("Max Capacity"), "fieldname": "max_capacity", "fieldtype": "Int", "width": 100},
        {"label": _("Enrolled"), "fieldname": "enrolled_count", "fieldtype": "Int", "width": 80},
        {"label": _("Present"), "fieldname": "present_count", "fieldtype": "Int", "width": 80},
        {"label": _("Absent"), "fieldname": "absent_count", "fieldtype": "Int", "width": 80},
        {"label": _("Attendance %"), "fieldname": "attendance_pct", "fieldtype": "Percent", "width": 110},
        {"label": _("Utilization %"), "fieldname": "utilization_pct", "fieldtype": "Percent", "width": 110},
    ]

def get_data(filters):
    conditions = "WHERE yc.docstatus = 1"
    values = {}
    if filters.get("from_date"):
        conditions += " AND yc.class_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND yc.class_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    if filters.get("instructor"):
        conditions += " AND yc.instructor = %(instructor)s"
        values["instructor"] = filters["instructor"]

    classes = frappe.db.sql(f"""
        SELECT yc.name, yc.class_name, yc.class_type, yc.instructor,
               yc.class_date, yc.max_capacity, yc.enrolled_count
        FROM `tabYoga Class` yc {conditions}
        ORDER BY yc.class_date DESC
    """, values, as_dict=True)

    for c in classes:
        att = frappe.db.get_value("Attendance Record", {"yoga_class": c.name}, "name")
        present = absent = 0
        if att:
            present = frappe.db.count("Attendance Student", filters={"parent": att, "status": "Present"})
            absent = frappe.db.count("Attendance Student", filters={"parent": att, "status": "Absent"})
        c.present_count = present
        c.absent_count = absent
        c.attendance_pct = round((present / c.enrolled_count * 100) if c.enrolled_count else 0, 2)
        c.utilization_pct = round((c.enrolled_count / c.max_capacity * 100) if c.max_capacity else 0, 2)

    return classes
