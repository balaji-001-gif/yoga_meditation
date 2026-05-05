import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label":_("Month"),"fieldname":"month","fieldtype":"Data","width":100},
        {"label":_("Total Bookings"),"fieldname":"total_bookings","fieldtype":"Int","width":120},
        {"label":_("Paid Bookings"),"fieldname":"paid_bookings","fieldtype":"Int","width":120},
        {"label":_("Total Revenue"),"fieldname":"total_revenue","fieldtype":"Currency","width":130},
        {"label":_("Package Revenue"),"fieldname":"pkg_revenue","fieldtype":"Currency","width":130},
        {"label":_("Class Revenue"),"fieldname":"cls_revenue","fieldtype":"Currency","width":130},
        {"label":_("New Students"),"fieldname":"new_students","fieldtype":"Int","width":110},
    ]

def get_data(filters):
    conditions = "WHERE docstatus = 1"
    values = {}
    if filters.get("year"):
        conditions += " AND YEAR(booking_date) = %(year)s"
        values["year"] = filters["year"]
    rows = frappe.db.sql(f"""
        SELECT DATE_FORMAT(booking_date,'%%Y-%%m') as month,
               COUNT(*) as total_bookings,
               SUM(CASE WHEN payment_status='Paid' THEN 1 ELSE 0 END) as paid_bookings,
               SUM(net_amount) as total_revenue,
               SUM(CASE WHEN booking_type='Wellness Package' THEN net_amount ELSE 0 END) as pkg_revenue,
               SUM(CASE WHEN booking_type='Single Class' THEN net_amount ELSE 0 END) as cls_revenue
        FROM `tabBooking` {conditions}
        GROUP BY DATE_FORMAT(booking_date,'%%Y-%%m')
        ORDER BY month DESC
    """, values, as_dict=True)
    for row in rows:
        ym = row.month.split("-")
        new_students = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabStudent Member`
            WHERE YEAR(creation)=%s AND MONTH(creation)=%s
        """, (ym[0], ym[1]))[0][0]
        row.new_students = new_students
    return rows
