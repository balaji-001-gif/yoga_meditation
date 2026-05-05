import frappe
from frappe import _
from frappe.utils import today

@frappe.whitelist()
def get_student_dashboard(student):
    """Return dashboard data for a student."""
    student_doc = frappe.get_doc("Student Member", student)
    bookings = frappe.get_all("Booking", filters={"student": student, "docstatus": 1},
                              fields=["name", "booking_type", "booking_date", "booking_status", "net_amount"],
                              order_by="booking_date desc", limit=10)
    goals = frappe.get_all("Wellness Goal", filters={"student": student},
                           fields=["goal_title", "goal_type", "status", "progress_pct"])
    trackers = frappe.get_all("Progress Tracker", filters={"student": student},
                              fields=["tracking_date", "mood_score", "mindfulness_score", "flexibility_score"],
                              order_by="tracking_date desc", limit=5)
    return {
        "student": student_doc.as_dict(),
        "recent_bookings": bookings,
        "wellness_goals": goals,
        "progress_history": trackers
    }

@frappe.whitelist()
def record_payment(booking, amount):
    """Mark a booking as paid."""
    doc = frappe.get_doc("Booking", booking)
    doc.payment_status = "Paid"
    doc.save(ignore_permissions=True)
    frappe.msgprint(_("Payment recorded for Booking {0}").format(booking))
    return {"status": "success"}

@frappe.whitelist()
def add_session_participant(session, student):
    """Add a student to a meditation session."""
    sess = frappe.get_doc("Meditation Session", session)
    exists = any(r.student == student for r in sess.participants)
    if exists:
        frappe.throw(_("Student is already registered for this session."))
    if len(sess.participants) >= (sess.max_participants or 15):
        frappe.throw(_("Session is full. No available spots."))
    sess.append("participants", {
        "student": student,
        "attendance_status": "Registered"
    })
    sess.save(ignore_permissions=True)
    return {"status": "success", "message": "Participant added successfully."}

@frappe.whitelist()
def get_available_classes(date=None):
    """Get all available yoga classes for a given date."""
    filters = {"status": "Scheduled", "docstatus": 1}
    if date:
        filters["class_date"] = date
    classes = frappe.get_all("Yoga Class", filters=filters,
                             fields=["name", "class_name", "class_type", "instructor",
                                     "class_date", "start_time", "available_slots", "fee_per_class"])
    return classes

@frappe.whitelist()
def quick_book(student, yoga_class):
    """Quick book a student into a yoga class."""
    cls = frappe.get_doc("Yoga Class", yoga_class)
    if cls.available_slots <= 0:
        frappe.throw(_("No available slots in this class."))
    booking = frappe.new_doc("Booking")
    booking.student = student
    booking.booking_type = "Single Class"
    booking.yoga_class = yoga_class
    booking.booking_date = today()
    booking.amount = cls.fee_per_class or 0
    booking.insert(ignore_permissions=True)
    booking.submit()
    return {"booking": booking.name, "status": "confirmed"}

@frappe.whitelist()
def get_instructor_schedule(instructor, from_date=None, to_date=None):
    """Get schedule for a specific instructor."""
    filters = {"instructor": instructor, "docstatus": 1}
    if from_date:
        filters["class_date"] = (">=", from_date)
    if to_date:
        filters["class_date"] = ("<=", to_date)
    classes = frappe.get_all("Yoga Class", filters=filters,
                             fields=["name", "class_name", "class_date", "start_time",
                                     "end_time", "enrolled_count", "max_capacity", "status"])
    return classes
