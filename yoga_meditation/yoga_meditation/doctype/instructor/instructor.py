import frappe
from frappe.model.document import Document

class Instructor(Document):
    def validate(self):
        if self.available_from and self.available_to:
            if self.available_from >= self.available_to:
                frappe.throw("Available From time must be before Available To time.")

    def get_upcoming_classes(self):
        return frappe.get_all("Yoga Class", filters={"instructor": self.name, "status": "Scheduled"}, fields=["*"])
