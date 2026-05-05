import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Student"), "fieldname": "student", "fieldtype": "Link", "options": "Student Member", "width": 150},
        {"label": _("Student Name"), "fieldname": "student_name", "fieldtype": "Data", "width": 150},
        {"label": _("Membership Type"), "fieldname": "membership_type", "fieldtype": "Data", "width": 130},
        {"label": _("Classes Attended"), "fieldname": "classes_attended", "fieldtype": "Int", "width": 120},
        {"label": _("Meditation Sessions"), "fieldname": "meditation_sessions", "fieldtype": "Int", "width": 140},
        {"label": _("Avg Mood Score"), "fieldname": "avg_mood", "fieldtype": "Float", "width": 120},
        {"label": _("Avg Mindfulness"), "fieldname": "avg_mindfulness", "fieldtype": "Float", "width": 130},
        {"label": _("Goals Active"), "fieldname": "goals_active", "fieldtype": "Int", "width": 100},
        {"label": _("Goals Achieved"), "fieldname": "goals_achieved", "fieldtype": "Int", "width": 110},
        {"label": _("Last Activity"), "fieldname": "last_activity", "fieldtype": "Date", "width": 110},
    ]

def get_data(filters):
    conditions = "WHERE 1=1"
    values = {}
    if filters.get("student"):
        conditions += " AND sm.name = %(student)s"
        values["student"] = filters["student"]
    if filters.get("membership_status"):
        conditions += " AND sm.membership_status = %(membership_status)s"
        values["membership_status"] = filters["membership_status"]

    students = frappe.db.sql(f"""
        SELECT sm.name as student, sm.full_name as student_name, sm.membership_type,
               sm.classes_used as classes_attended
        FROM `tabStudent Member` sm
        {conditions}
        ORDER BY sm.full_name
    """, values, as_dict=True)

    for s in students:
        # Meditation sessions attended
        sess_count = frappe.db.count("Session Participant", filters={"student": s.student, "attendance_status": "Present"})
        s.meditation_sessions = sess_count

        # Progress tracker averages
        progress = frappe.db.sql("""
            SELECT AVG(mood_score) as avg_mood, AVG(mindfulness_score) as avg_mindfulness
            FROM `tabProgress Tracker` WHERE student = %s
        """, s.student, as_dict=True)
        if progress:
            s.avg_mood = round(progress[0].avg_mood or 0, 2)
            s.avg_mindfulness = round(progress[0].avg_mindfulness or 0, 2)

        # Goals
        s.goals_active = frappe.db.count("Wellness Goal", filters={"student": s.student, "status": "Active"})
        s.goals_achieved = frappe.db.count("Wellness Goal", filters={"student": s.student, "status": "Achieved"})

        # Last activity
        last_tracker = frappe.db.get_value("Progress Tracker", {"student": s.student}, "tracking_date", order_by="tracking_date desc")
        s.last_activity = last_tracker

    return students
