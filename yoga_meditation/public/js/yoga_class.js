frappe.ui.form.on("Yoga Class", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Mark Attendance"), function () {
                frappe.model.open_mapped_doc({
                    method: "yoga_meditation.yoga_meditation.doctype.yoga_class.yoga_class.make_attendance",
                    frm: frm
                });
            }, __("Actions"));

            frm.add_custom_button(__("Add Student"), function () {
                let d = new frappe.ui.Dialog({
                    title: "Add Student to Class",
                    fields: [
                        {fieldtype:"Link", fieldname:"student", label:"Student", options:"Student Member", reqd:1}
                    ],
                    primary_action_label: "Add",
                    primary_action(values) {
                        frappe.call({
                            method: "yoga_meditation.yoga_meditation.doctype.yoga_class.yoga_class.add_student",
                            args: {docname: frm.doc.name, student: values.student},
                            callback(r) {
                                if (!r.exc) { frm.reload_doc(); d.hide(); }
                            }
                        });
                    }
                });
                d.show();
            }, __("Actions"));
        }

        // Show capacity bar
        if (frm.doc.max_capacity) {
            let pct = Math.round((frm.doc.enrolled_count / frm.doc.max_capacity) * 100);
            let color = pct >= 90 ? "red" : pct >= 70 ? "orange" : "green";
            frm.dashboard.add_comment(
                `<div><strong>Capacity:</strong> ${frm.doc.enrolled_count}/${frm.doc.max_capacity} 
                <div style="background:#eee;border-radius:4px;height:8px;width:200px;display:inline-block;margin-left:8px;">
                <div style="background:${color};height:8px;border-radius:4px;width:${pct}%"></div></div>
                <span style="color:${color};margin-left:8px;">${pct}%</span></div>`,
                "blue", true
            );
        }
    },

    start_time(frm) {
        if (frm.doc.start_time && frm.doc.duration_minutes) {
            // Auto-calculate end time
            let [h, m] = frm.doc.start_time.split(":").map(Number);
            let endMins = h * 60 + m + (frm.doc.duration_minutes || 60);
            frm.set_value("end_time", `${String(Math.floor(endMins/60)).padStart(2,"0")}:${String(endMins%60).padStart(2,"0")}:00`);
        }
    }
});
