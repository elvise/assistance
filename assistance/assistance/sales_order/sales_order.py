# -*- coding: utf-8 -*-
# Copyright (c) 2017, Syed Abdul Qadeer and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import frappe.utils
from frappe.model.mapper import get_mapped_doc

def on_submit(self, method):
	for item in self.get("purposes"):
		if not (item.prevdoc_doctype and item.prevdoc_doctype == "Sales Order" and
				item.prevdoc_docname and item.serial_no):
			return

		if not frappe.db.sql("""select name from `tabSales Order` where name=%s""", item.prevdoc_docname):
			return

		serial_no_data = frappe.db.get_value("Sales Order Item", {
			"parent": item.prevdoc_docname,
			"parenttype": item.prevdoc_doctype,
			"item_code": item.item_code
		}, ["serial_no", "name"])

		if serial_no_data:
			splitted = []
			if serial_no_data[0]:
				splitted = serial_no_data[0].split("\n")
			if item.serial_no not in splitted:
				splitted.append(item.serial_no)

			joined = "\n".join(splitted)

			frappe.db.set_value("Sales Order Item", serial_no_data[1], "serial_no", joined,
								update_modified=False)

def on_cancel(self, method):
	pass

@frappe.whitelist()
def make_assistance(source_name, target_doc=None):
	visit = frappe.db.sql("""select t1.name
		from `tabAssistance` t1, `tabAssistance Visit Purpose` t2
		where t2.parent=t1.name and t2.prevdoc_docname=%s
		and t1.docstatus=1 and t1.completion_status='Fully Completed'""", source_name)

	if not visit:
		doclist = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Assistance",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Sales Order Item": {
				"doctype": "Assistance Visit Purpose",
				"field_map": {
					"parent": "prevdoc_docname",
					"parenttype": "prevdoc_doctype",
					"name": "prevdoc_detail_docname"
				},
				"add_if_empty": True
			}
		}, target_doc)

		return doclist