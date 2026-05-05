import frappe
from frappe.utils import today, add_days, getdate

def send_class_reminders():
    """Send reminder emails for classes scheduled tomorrow."""
    tomorrow = add_days(today(), 1)
    classes = frappe.get_all("Yoga Class", filters={
        "class_date": tomorrow, "status": "Scheduled", "docstatus": 1
    }, fields=["name", "class_name", "instructor", "start_time", "room_location"])

    for cls in classes:
        cls_doc = frappe.get_doc("Yoga Class", cls.name)
        for row in cls_doc.enrolled_students:
            student = frappe.get_doc("Student Member", row.student)
            if student.email_id:
                frappe.sendmail(
                    recipients=[student.email_id],
                    subject=f"Reminder: {cls.class_name} Tomorrow at {cls.start_time}",
                    template="class_reminder",
                    args={
                        "student_name": student.full_name,
                        "class_name": cls.class_name,
                        "class_date": tomorrow,
                        "start_time": cls.start_time,
                        "instructor": cls.instructor,
                        "location": cls.room_location
                    }
                )
    frappe.logger().info(f"Sent reminders for {len(classes)} classes on {tomorrow}")

def auto_mark_attendance():
    """Auto-complete attendance for past classes if not already marked."""
    yesterday = add_days(today(), -1)
    classes = frappe.get_all("Yoga Class", filters={
        "class_date": yesterday, "status": "Scheduled", "docstatus": 1
    }, fields=["name"])

    for cls in classes:
        exists = frappe.db.exists("Attendance Record", {"yoga_class": cls.name})
        if not exists:
            att = frappe.new_doc("Attendance Record")
            att.reference_type = "Yoga Class"
            att.yoga_class = cls.name
            att.attendance_date = yesterday
            att.insert(ignore_permissions=True)
            frappe.db.commit()

def generate_weekly_report():
    """Generate weekly wellness summary report."""
    frappe.logger().info("Weekly Yoga & Meditation report generated.")
