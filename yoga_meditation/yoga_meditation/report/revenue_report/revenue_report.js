frappe.query_reports["Revenue Report"] = {
    filters: [
        {fieldname:"year",label:__("Year"),fieldtype:"Select",
         options:["2023","2024","2025","2026"],default:new Date().getFullYear().toString()}
    ]
};
