frappe.query_reports["Student Progress Report"] = {
    filters: [
        {
            fieldname: "student",
            label: __("Student"),
            fieldtype: "Link",
            options: "Student Member"
        },
        {
            fieldname: "membership_status",
            label: __("Membership Status"),
            fieldtype: "Select",
            options: "\nActive\nInactive\nExpired\nSuspended"
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        }
    ]
};
