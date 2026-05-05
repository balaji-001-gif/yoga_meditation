app_name = "yoga_meditation"
app_title = "Yoga Meditation"
app_publisher = "Your Company"
app_description = "Yoga & Meditation Management App for ERPNext v15+"
app_email = "hello@yourcompany.com"
app_license = "MIT"
app_version = "1.0.0"

required_apps = ["frappe", "erpnext"]

# ─── DocType JS ───────────────────────────────
doctype_js = {
    "Yoga Class": "public/js/yoga_class.js",
    "Meditation Session": "public/js/meditation_session.js",
    "Student Member": "public/js/student_member.js",
    "Booking": "public/js/booking.js",
}

# ─── Scheduled Tasks ──────────────────────────
scheduler_events = {
    "daily": [
        "yoga_meditation.yoga_meditation.tasks.send_class_reminders",
        "yoga_meditation.yoga_meditation.tasks.auto_mark_attendance",
    ],
    "weekly": [
        "yoga_meditation.yoga_meditation.tasks.generate_weekly_report",
    ],
}

# ─── On Submit Events ─────────────────────────
doc_events = {
    "Booking": {
        "on_submit": "yoga_meditation.yoga_meditation.doctype.booking.booking.on_booking_submit",
        "on_cancel": "yoga_meditation.yoga_meditation.doctype.booking.booking.on_booking_cancel",
    },
    "Attendance Record": {
        "after_insert": "yoga_meditation.yoga_meditation.doctype.attendance_record.attendance_record.update_class_count",
    },
}

# ─── Website Routes ───────────────────────────
website_route_rules = [
    {"from_route": "/yoga-classes", "to_route": "yoga_class"},
    {"from_route": "/wellness-packages", "to_route": "wellness_package"},
]

# ─── Fixtures ─────────────────────────────────
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Yoga Meditation"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Yoga Meditation"]]},
    {"dt": "Notification", "filters": [["module", "=", "Yoga Meditation"]]},
]

# ─── After Install ────────────────────────────
after_install = "yoga_meditation.yoga_meditation.install.after_install"

# ─── App Brand Color ──────────────────────────
brand_html = "<span class='brand-logo'>🧘 Yoga & Meditation</span>"
