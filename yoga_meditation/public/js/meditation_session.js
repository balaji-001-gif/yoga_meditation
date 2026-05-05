frappe.ui.form.on("Meditation Session", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Add Participant"), function () {
                let d = new frappe.ui.Dialog({
                    title: "Add Participant",
                    fields: [{fieldtype:"Link", fieldname:"student", label:"Student", options:"Student Member", reqd:1}],
                    primary_action_label: "Add",
                    primary_action(values) {
                        frappe.call({
                            method: "yoga_meditation.yoga_meditation.api.add_session_participant",
                            args: {session: frm.doc.name, student: values.student},
                            callback(r) { if (!r.exc) { frm.reload_doc(); d.hide(); } }
                        });
                    }
                });
                d.show();
            }, __("Actions"));
        }
    }
});
