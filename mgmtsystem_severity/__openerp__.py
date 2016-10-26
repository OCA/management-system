# -*- coding: utf-8 -*-
# Copyright 2015 Savoir-faire Linux <https://www.savoirfairelinux.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System Severity",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        "mgmtsystem",
    ],
    "data": [
        "views/mgmtsystem_severity.xml",
        "security/ir.model.access.csv",
        "data/mgmtsystem_severity.xml",
    ],
    "demo": [],
    "installable": True,
}
