import frappe
from frappe.model.document import Document

class MeditationSession(Document):
    def validate(self):
        self.registered_count = len(self.participants or [])
        self.available_spots = (self.max_participants or 0) - self.registered_count

    def on_submit(self):
        self.status = "Scheduled"
