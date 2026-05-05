import frappe
from frappe.utils import add_days, nowdate, add_to_date

def create_demo_data():
    """Main entry point to create demo data."""
    print("Starting demo data creation...")
    
    # 1. Ensure Yoga Types exist (normally handled by after_install, but good to be safe)
    create_yoga_types()
    
    # 2. Create Instructors
    create_instructors()
    
    # 3. Create Student Members
    create_students()
    
    # 4. Create Wellness Packages
    create_packages()
    
    # 5. Create Yoga Classes and Meditation Sessions
    create_classes_and_sessions()
    
    # 6. Create some Bookings
    create_bookings()
    
    frappe.db.commit()
    print("Demo data creation completed successfully!")

def create_yoga_types():
    types = ["Hatha", "Vinyasa", "Ashtanga", "Yin", "Restorative"]
    for t in types:
        if not frappe.db.exists("Yoga Type", t):
            frappe.get_doc({
                "doctype": "Yoga Type",
                "yoga_type_name": t
            }).insert()

def create_instructors():
    instructors = [
        {"name": "Sarah Zen", "email": "sarah@yoga.com", "specialty": "Hatha"},
        {"name": "Mike Flow", "email": "mike@yoga.com", "specialty": "Vinyasa"},
        {"name": "Elena Peace", "email": "elena@yoga.com", "specialty": "Yin"}
    ]
    for ins in instructors:
        if not frappe.db.exists("Instructor", {"full_name": ins["name"]}):
            doc = frappe.get_doc({
                "doctype": "Instructor",
                "full_name": ins["name"],
                "email_id": ins["email"],
                "is_active": 1,
                "years_experience": 5
            })
            # Add specialization
            doc.append("specializations", {"yoga_type": ins["specialty"]})
            doc.insert()

def create_students():
    students = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"}
    ]
    for s in students:
        if not frappe.db.exists("Student Member", {"full_name": s["name"]}):
            frappe.get_doc({
                "doctype": "Student Member",
                "full_name": s["name"],
                "email_id": s["email"],
                "membership_status": "Active"
            }).insert()

def create_packages():
    packages = [
        {"name": "10 Class Pass", "price": 150, "type": "Monthly"},
        {"name": "Unlimited Monthly", "price": 200, "type": "Monthly"}
    ]
    for p in packages:
        if not frappe.db.exists("Wellness Package", p["name"]):
            frappe.get_doc({
                "doctype": "Wellness Package",
                "package_name": p["name"],
                "package_type": p["type"],
                "price": p["price"]
            }).insert()

def create_classes_and_sessions():
    # Yoga Class
    if not frappe.db.exists("Yoga Class", {"class_name": "Morning Hatha"}):
        frappe.get_doc({
            "doctype": "Yoga Class",
            "class_name": "Morning Hatha",
            "class_type": "Yoga",
            "instructor": frappe.get_all("Instructor", limit=1)[0].name,
            "class_date": add_days(nowdate(), 1),
            "start_time": "08:00:00",
            "max_capacity": 20,
            "status": "Scheduled"
        }).insert()
    
    # Meditation Session
    if not frappe.db.exists("Meditation Session", {"session_title": "Evening Mindfulness"}):
        frappe.get_doc({
            "doctype": "Meditation Session",
            "session_title": "Evening Mindfulness",
            "meditation_type": "Mindfulness",
            "instructor": frappe.get_all("Instructor", limit=1)[0].name,
            "session_date": add_days(nowdate(), 1),
            "start_time": "18:00:00",
            "max_participants": 15,
            "status": "Scheduled"
        }).insert()

def create_bookings():
    student = frappe.get_all("Student Member", limit=1)
    yoga_class = frappe.get_all("Yoga Class", limit=1)
    
    if student and yoga_class:
        if not frappe.db.exists("Booking", {"student": student[0].name, "yoga_class": yoga_class[0].name}):
            frappe.get_doc({
                "doctype": "Booking",
                "student": student[0].name,
                "booking_type": "Single Class",
                "yoga_class": yoga_class[0].name,
                "booking_status": "Confirmed",
                "payment_status": "Paid"
            }).insert()

if __name__ == "__main__":
    create_demo_data()
