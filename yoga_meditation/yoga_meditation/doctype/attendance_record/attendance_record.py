import frappe
from frappe.model.document import Document

class AttendanceRecord(Document):
    def before_insert(self):
        self.populate_students()

    def populate_students(self):
        self.attendance_students = []
        if self.reference_type == "Yoga Class" and self.yoga_class:
            cls = frappe.get_doc("Yoga Class", self.yoga_class)
            for row in cls.enrolled_students:
                self.append("attendance_students", {
                    "student": row.student,
                    "student_name": row.student_name,
                    "status": "Present"
                })
        elif self.reference_type == "Meditation Session" and self.meditation_session:
            sess = frappe.get_doc("Meditation Session", self.meditation_session)
            for row in sess.participants:
                self.append("attendance_students", {
                    "student": row.student,
                    "student_name": row.student_name,
                    "status": "Present"
                })

def update_class_count(doc, method):
    for row in doc.attendance_students:
        if row.status == "Present":
            student = frappe.get_doc("Student Member", row.student)
            frappe.db.set_value("Student Member", row.student, "classes_used", (student.classes_used or 0) + 1)
            frappe.db.set_value("Student Member", row.student, "classes_remaining",
                                max(0, (student.classes_remaining or 0) - 1))
