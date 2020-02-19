# Copyright (C) 2018 - 2020 Ludovic Lelarge (<http://www.eta123.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Action - Claim",
    "version": "13.0.1.0.0",
    "author": "Ludovic Lelarge, Odoo Community Association (OCA)",
    "website": "www.eta123.be",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_action", "mgmtsystem_claim"],
    "data": [
        "views/mgmtsystem_action_views.xml", 
        "views/mgmtsystem_claim_views.xml"
    ],
    "installable": True,
}
