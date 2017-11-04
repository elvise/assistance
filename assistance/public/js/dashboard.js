frappe.ui.form.Dashboard.prototype.set_open_count = function() {
	if(!this.data.transactions || !this.data.fieldname) {
		return;
	}

	// list all items from the transaction list
	var items = [],
		me = this;

	this.data.transactions.forEach(function(group) {
		group.items.forEach(function(item) { items.push(item); });
	});

	var method = this.data.method || 'frappe.desk.notifications.get_open_count';

	var args = {
		doctype: this.frm.doctype,
		name: this.frm.doc.name
	}

	if(!this.data.method){
		args["dashboard_data"] = this.data;
	}

	frappe.call({
		type: "GET",
		method: method,
		args: args,
		callback: function(r) {
			if(r.message.timeline_data) {
				me.update_heatmap(r.message.timeline_data);
			}

			// update badges
			$.each(r.message.count, function(i, d) {
				me.frm.dashboard.set_badge_count(d.name, cint(d.open_count), cint(d.count));
			});

			// update from internal links
			$.each(me.data.internal_links, function(doctype, link) {
				var table_fieldname = link[0], link_fieldname = link[1];
				var names = [];
				(me.frm.doc[table_fieldname] || []).forEach(function(d) {
					var value = d[link_fieldname];
					if(value && names.indexOf(value)===-1) {
						names.push(value);
					}
				});
				me.frm.dashboard.set_badge_count(doctype, 0, names.length, names);
			});

			me.frm.dashboard_data = r.message;
			me.frm.trigger('dashboard_update');
		}
	});

}