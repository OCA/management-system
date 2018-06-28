# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Management System - Consent",
    "summary": "Allow people to accept inclusion in some system",
    "version": "10.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Management System",
    "website": "https://github.com/OCA/management-system",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mgmtsystem",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_actions_server.xml",
        "data/ir_cron.xml",
        "data/mail_template.xml",
        "templates/form.xml",
        "views/mgmtsystem_consent.xml",
        "views/mgmtsystem_system.xml",
        "views/res_partner.xml",
    ],
}
