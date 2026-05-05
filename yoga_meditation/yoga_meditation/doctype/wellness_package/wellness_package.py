import frappe
from frappe.model.document import Document

class WellnessPackage(Document):
    def validate(self):
        if self.discounted_price and self.discounted_price > self.price:
            frappe.throw("Discounted Price cannot be greater than the original Price.")

    def get_effective_price(self):
        return self.discounted_price if self.discounted_price else self.price
