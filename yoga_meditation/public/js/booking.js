frappe.ui.form.on("Booking", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.payment_status !== "Paid") {
            frm.add_custom_button(__("Record Payment"), function () {
                frappe.call({
                    method: "yoga_meditation.yoga_meditation.api.record_payment",
                    args: {booking: frm.doc.name, amount: frm.doc.net_amount},
                    callback(r) {
                        if (!r.exc) frm.reload_doc();
                    }
                });
            }, __("Actions"));
        }
        if (frm.doc.sales_invoice) {
            frm.add_custom_button(__("View Invoice"), function () {
                frappe.set_route("Form", "Sales Invoice", frm.doc.sales_invoice);
            });
        }
    },

    wellness_package(frm) {
        if (frm.doc.wellness_package) {
            frappe.db.get_value("Wellness Package", frm.doc.wellness_package, ["price","discounted_price"], function(v) {
                frm.set_value("amount", v.discounted_price || v.price);
            });
        }
    },

    yoga_class(frm) {
        if (frm.doc.yoga_class) {
            frappe.db.get_value("Yoga Class", frm.doc.yoga_class, "fee_per_class", function(v) {
                frm.set_value("amount", v.fee_per_class || 0);
            });
        }
    }
});
