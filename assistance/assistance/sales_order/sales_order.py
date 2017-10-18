# -*- coding: utf-8 -*-
# Copyright (c) 2017, Syed Abdul Qadeer and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import frappe.utils
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def make_maintenance_visit(source_name, target_doc=None):
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
					"parenttype": "prevdoc_doctype"
				},
				"add_if_empty": True
			}
		}, target_doc)

		return doclist