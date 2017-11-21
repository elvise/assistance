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

def before_save(self, method):
    update_sales_order_items(self)

def on_submit(self, method):
    for item in self.get("purposes"):
        if not (item.prevdoc_doctype and item.prevdoc_doctype == "Sales Order" and
                    item.prevdoc_docname and item.serial_no):
            continue

        if not frappe.db.sql("""select name from `tabSales Order` where name=%s""", item.prevdoc_docname):
            continue

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



def update_sales_order_items(self):
    from erpnext.stock.get_item_details import get_item_details
    from frappe.model.meta import default_fields

    sales_order_exists = (len(self.get("purposes", {"prevdoc_doctype": "Sales Order"})) > 0)

    if not sales_order_exists:
        return

    sales_order = get_sales_order(self)


    if not sales_order:
        return

    if not sales_order.docstatus == 0:
        return

    for item in self.get("purposes"):
        if item.prevdoc_docname or item.prevdoc_doctype:
            continue

        out = get_item_details({
            "item_code": item.item_code,
            "serial_no": item.serial_no,
            "warehouse": item.warehouse,
            "customer": sales_order.customer,
            "currency": sales_order.currency,
            "conversion_rate": sales_order.conversion_rate,
            "price_list": sales_order.selling_price_list,
            "price_list_currency": sales_order.price_list_currency,
            "plc_conversion_rate": sales_order.plc_conversion_rate,
            "company": sales_order.company,
            "order_type": sales_order.order_type,
            "transaction_date": sales_order.transaction_date,
            "ignore_pricing_rule": sales_order.ignore_pricing_rule,
            "doctype": sales_order.doctype,
            "name": sales_order.name,
            "project": sales_order.project,
            "qty": item.qty or 1,
            "stock_qty": None,
            "conversion_factor": None,
            "is_pos": 0,
            "update_stock": 0
        })

        del out["doctype"]
        del out["name"]

        child_item = sales_order.append("items", {})

        for key, value in out.items():
            if key not in default_fields and hasattr(child_item, key):
                child_item.set(key, value, as_value=True)

        sales_order.save()
        #frappe.db.set_value("Assistance Visit Purpose", item.name, "prevdoc_detail_docname", joined,
        #                    update_modified=False)
        item.prevdoc_detail_docname = child_item.name
        item.prevdoc_doctype = sales_order.doctype
        item.prevdoc_docname = sales_order.name

    pass


def get_sales_order(self):
    sales_order = None
    for item in self.get("purposes", {"prevdoc_doctype": "Sales Order"}):
        if not item.prevdoc_docname or not (item.prevdoc_doctype and
                                                    item.prevdoc_doctype == "Sales Order"):
            continue

        if not sales_order:
            sales_order = frappe.get_doc("Sales Order", item.prevdoc_docname)

        elif not sales_order.name == item.prevdoc_docname:
            frappe.throw(_("You cannot have multiple Sales Order in the Assistance"))

    return sales_order


def on_cancel(self, method):
    pass
