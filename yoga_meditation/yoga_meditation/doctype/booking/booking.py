import frappe
from frappe.model.document import Document
from frappe.utils import add_days

class Booking(Document):
    def validate(self):
        self.calculate_net_amount()
        self.set_package_end_date()

    def calculate_net_amount(self):
        self.net_amount = (self.amount or 0) - (self.discount or 0)

    def set_package_end_date(self):
        if self.booking_type == "Wellness Package" and self.wellness_package and self.package_start_date:
            pkg = frappe.get_doc("Wellness Package", self.wellness_package)
            self.package_end_date = add_days(self.package_start_date, pkg.validity_days or 30)

    def on_submit(self):
        self.booking_status = "Confirmed"
        self.create_sales_invoice()
        self.enroll_student_in_class()
        self.send_booking_confirmation()

    def on_cancel(self):
        self.booking_status = "Cancelled"

    def create_sales_invoice(self):
        if self.net_amount > 0 and not self.sales_invoice:
            student = frappe.get_doc("Student Member", self.student)
            if not student.customer:
                return
            inv = frappe.new_doc("Sales Invoice")
            inv.customer = student.customer
            inv.due_date = frappe.utils.today()
            inv.append("items", {
                "item_name": self.booking_type,
                "description": f"Booking: {self.name}",
                "qty": 1,
                "rate": self.net_amount,
                "amount": self.net_amount
            })
            inv.insert(ignore_permissions=True)
            self.db_set("sales_invoice", inv.name)
            frappe.msgprint(f"Sales Invoice {inv.name} created.")

    def enroll_student_in_class(self):
        if self.booking_type == "Single Class" and self.yoga_class:
            cls = frappe.get_doc("Yoga Class", self.yoga_class)
            exists = any(r.student == self.student for r in cls.enrolled_students)
            if not exists:
                cls.append("enrolled_students", {
                    "student": self.student,
                    "enrollment_date": frappe.utils.today(),
                    "payment_status": "Paid" if self.payment_status == "Paid" else "Pending"
                })
                cls.save(ignore_permissions=True)

    def send_booking_confirmation(self):
        student = frappe.get_doc("Student Member", self.student)
        if student.email_id:
            frappe.sendmail(
                recipients=[student.email_id],
                subject=f"Booking Confirmed - {self.name}",
                template="booking_confirmation",
                args={"booking_id": self.name, "student_name": student.full_name,
                      "booking_type": self.booking_type, "booking_date": self.booking_date}
            )

def on_booking_submit(doc, method):
    pass

def on_booking_cancel(doc, method):
    pass
