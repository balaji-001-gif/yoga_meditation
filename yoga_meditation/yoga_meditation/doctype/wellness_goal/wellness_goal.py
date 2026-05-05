import frappe
from frappe.model.document import Document

class WellnessGoal(Document):
    def validate(self):
        if self.target_value and self.current_value is not None:
            if self.target_value > 0:
                self.progress_pct = round((self.current_value / self.target_value) * 100, 2)
            if self.progress_pct >= 100:
                self.status = "Achieved"
