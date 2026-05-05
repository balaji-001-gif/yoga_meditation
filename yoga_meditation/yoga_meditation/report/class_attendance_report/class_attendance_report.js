frappe.query_reports["Class Attendance Report"] = {
    filters: [
        {fieldname:"from_date",label:__("From Date"),fieldtype:"Date",default:frappe.datetime.add_months(frappe.datetime.get_today(),-1)},
        {fieldname:"to_date",label:__("To Date"),fieldtype:"Date",default:frappe.datetime.get_today()},
        {fieldname:"instructor",label:__("Instructor"),fieldtype:"Link",options:"Instructor"},
        {fieldname:"class_type",label:__("Class Type"),fieldtype:"Select",options:"\nYoga\nMeditation\nYoga + Meditation\nWorkshop"}
    ]
};
