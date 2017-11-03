var assistance_sales_order_onload = cur_frm.cscript.onload;
var assistance_sales_order_refresh = cur_frm.cscript.refresh;

cur_frm.cscript.onload = function(doc, dt, dn){
	if(assistance_sales_order_onload){
	    assistance_sales_order_onload.apply(this, [doc, dt, dn]);
	}

    cur_frm.meta.__dashboard = {
		'fieldname': 'sales_order',
		'non_standard_fieldnames': {
			'Delivery Note': 'against_sales_order',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Subscription': 'reference_document',
			'Assistance': 'prevdoc_docname'
		},
		'internal_links': {
			'Quotation': ['items', 'prevdoc_docname'],
		},
		'transactions': [
			{
				'label': __('Fulfillment'),
				'items': ['Sales Invoice', 'Delivery Note']
			},
			{
				'label': __('Purchasing'),
				'items': ['Material Request', 'Purchase Order']
			},
			{
				'label': __('Projects'),
				'items': ['Project']
			},
			{
				'label': __('Assistance'),
				'items': ['Assistance']
			},
			{
				'label': __('Manufacturing'),
				'items': ['Production Order']
			},
			{
				'label': __('Reference'),
				'items': ['Quotation', 'Subscription']
			},
			{
				'label': __('Payment'),
				'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
			},
		]
	}

	cur_frm.dashboard.data = cur_frm.meta.__dashboard;
	cur_frm.dashboard.data_rendered = false;
	cur_frm.dashboard.transactions_area.empty();

	cur_frm.dashboard.refresh();
}

cur_frm.cscript.refresh = function(doc, dt, dn){
	if(assistance_sales_order_refresh){
		assistance_sales_order_refresh.apply(this, [doc, dt, dn]);
	}

	if(doc.docstatus == 1){
		// maintenance
		if(flt(doc.per_delivered, 2) < 100) {
			cur_frm.add_custom_button(__('Assistance'),
				function() { cur_frm.cscript.make_assistance() }, __("Make"));
		}
	}
}

cur_frm.cscript.make_assistance= function() {
	frappe.model.open_mapped_doc({
		method: "assistance.assistance.sales_order.sales_order.make_assistance",
		frm: this.frm
	})
}