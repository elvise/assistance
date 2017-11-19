# -*- coding: utf-8 -*-
# Copyright (c) 2017, Syed Abdul Qadeer and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import frappe.utils
from frappe import _

def validate(self, method):
    for d in self.get('purposes'):
        if d.serial_no and not frappe.db.exists({
            "doctype": "Serial No",
            "warehouse": d.warehouse,
            "item_code": d.item_code
        }, d.serial_no):
            frappe.throw(_("Serial No {0} does not exist").format(d.serial_no))

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
			"item_code": item.item_code,
            "name": item.prevdoc_detail_docname
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

