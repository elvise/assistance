var sales_order_onload = cur_frm.cscript.onload;

cur_frm.cscript.onload = function(doc, dt, dn){
    sales_order_onload.apply(null, [doc, dt, dn]);

    cur_frm.meta.__dashboard = {
		'fieldname': 'sales_order',
		'non_standard_fieldnames': {
			'Delivery Note': 'against_sales_order',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Subscription': 'reference_document',
		},
		'internal_links': {
			'Quotation': ['items', 'prevdoc_docname'],
			'Assistance': ['items', 'prevdoc_docname']
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
}