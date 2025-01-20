# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Nonconformity Hazard",
    "version": "17.0.1.0.0",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_hazard", "mgmtsystem_nonconformity"],
    "data": [
        "views/mgmtsystem_hazard.xml",
        "views/mgmtsystem_nonconformity.xml",
    ],
    "autoinstall": True,
}
