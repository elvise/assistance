# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "assistance"
app_title = "Assistance"
app_publisher = "Syed Abdul Qadeer"
app_description = "Assistance App"
app_icon = "fa fa-file-text"
app_color = "grey"
app_email = "sdqadeer44@gmail.com"
app_license = "Proprietary"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/assistance/css/assistance.css"
app_include_js = "/assets/js/assistance.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/assistance/css/assistance.css"
# web_include_js = "/assets/assistance/js/assistance.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Order" : "assistance/sales_order/sales_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "assistance.utils.get_home_page"

# Fixtures
# --------
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": {
            "fieldname": [
                "in", [
                    "serial_no"
                ]
            ]
        }
    }
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "assistance.install.before_install"
# after_install = "assistance.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "assistance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
 	"Assistance": {
 		"on_submit": "assistance.assistance.sales_order.sales_order.on_submit",
 		"on_cancel": "assistance.assistance.sales_order.sales_order.on_cancel",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"assistance.tasks.all"
# 	],
# 	"daily": [
# 		"assistance.tasks.daily"
# 	],
# 	"hourly": [
# 		"assistance.tasks.hourly"
# 	],
# 	"weekly": [
# 		"assistance.tasks.weekly"
# 	]
# 	"monthly": [
# 		"assistance.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "assistance.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.desk.notifications.get_open_count": "assistance.desk.notifications.get_open_count"
}

