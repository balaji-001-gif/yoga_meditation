frappe.ui.form.on("Student Member", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Booking History"), function () {
                frappe.set_route("List", "Booking", {student: frm.doc.name});
            });
            frm.add_custom_button(__("View Progress"), function () {
                frappe.set_route("List", "Progress Tracker", {student: frm.doc.name});
            });
            frm.add_custom_button(__("New Booking"), function () {
                frappe.new_doc("Booking", {student: frm.doc.name, student_name: frm.doc.full_name});
            }, __("Actions"));
        }

        // Membership status indicator
        let status = frm.doc.membership_status;
        let color = {"Active":"green","Inactive":"grey","Expired":"red","Suspended":"orange"}[status] || "grey";
        frm.dashboard.set_headline(`<span style="color:${color};font-weight:bold;">● ${status}</span>`);

        // Classes remaining progress
        if (frm.doc.total_classes_purchased > 0) {
            let remaining = frm.doc.classes_remaining;
            let total = frm.doc.total_classes_purchased;
            frm.dashboard.add_comment(
                `<strong>Classes Remaining:</strong> ${remaining} / ${total}`, "blue", true
            );
        }
    }
});
