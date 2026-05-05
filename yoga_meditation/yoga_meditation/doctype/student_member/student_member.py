import frappe
from frappe.model.document import Document

class StudentMember(Document):
    def before_save(self):
        self.calculate_classes_remaining()

    def calculate_classes_remaining(self):
        self.classes_remaining = (self.total_classes_purchased or 0) - (self.classes_used or 0)

    def after_insert(self):
        if not self.customer:
            self.create_erpnext_customer()

    def create_erpnext_customer(self):
        customer = frappe.new_doc("Customer")
        customer.customer_name = self.full_name
        customer.customer_type = "Individual"
        customer.customer_group = "Wellness Members"
        customer.territory = frappe.db.get_single_value("Selling Settings", "territory") or "All Territories"
        customer.insert(ignore_permissions=True)
        self.db_set("customer", customer.name)
        frappe.msgprint(f"Customer {customer.name} created successfully.")

    def get_booking_history(self):
        return frappe.get_all("Booking", filters={"student": self.name}, fields=["*"], order_by="booking_date desc")
