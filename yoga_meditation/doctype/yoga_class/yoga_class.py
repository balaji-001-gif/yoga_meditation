import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_seconds

class YogaClass(Document):
    def validate(self):
        self.set_duration()
        self.calculate_available_slots()
        self.validate_instructor_availability()

    def set_duration(self):
        if self.start_time and self.end_time:
            diff = time_diff_in_seconds(self.end_time, self.start_time)
            self.duration_minutes = int(diff / 60)

    def calculate_available_slots(self):
        self.enrolled_count = len(self.enrolled_students or [])
        self.available_slots = (self.max_capacity or 0) - self.enrolled_count

    def validate_instructor_availability(self):
        if self.instructor and self.class_date and self.start_time:
            conflict = frappe.db.exists("Yoga Class", {
                "instructor": self.instructor,
                "class_date": self.class_date,
                "start_time": self.start_time,
                "name": ("!=", self.name),
                "status": ("in", ["Scheduled", "In Progress"]),
                "docstatus": ("!=", 2)
            })
            if conflict:
                frappe.throw(f"Instructor {self.instructor} already has a class at this time on {self.class_date}.")

    def on_submit(self):
        self.status = "Scheduled"
        self.send_class_confirmation_notifications()

    def on_cancel(self):
        self.status = "Cancelled"
        self.notify_students_of_cancellation()

    def send_class_confirmation_notifications(self):
        for row in self.enrolled_students:
            student = frappe.get_doc("Student Member", row.student)
            if student.email_id:
                frappe.sendmail(
                    recipients=[student.email_id],
                    subject=f"Class Confirmed: {self.class_name}",
                    template="class_confirmation",
                    args={"class_name": self.class_name, "class_date": self.class_date,
                          "start_time": self.start_time, "instructor": self.instructor,
                          "student_name": student.full_name}
                )

    def notify_students_of_cancellation(self):
        for row in self.enrolled_students:
            student = frappe.get_doc("Student Member", row.student)
            if student.email_id:
                frappe.sendmail(
                    recipients=[student.email_id],
                    subject=f"Class Cancelled: {self.class_name}",
                    template="class_cancellation",
                    args={"class_name": self.class_name, "class_date": self.class_date,
                          "student_name": student.full_name}
                )
