# Copyright (C) 2025 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Risks",
    "summary": "Manage risks probability and severity",
    "version": "19.0.1.0.0",
    "author": "Gray Matter Logic, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management Systems",
    "depends": [
        "mgmtsystem",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/mgmtsystem_risk_probability.xml",
        "views/mgmtsystem_risk_severity.xml",
    ],
    "demo": [
        "demo/mgmtsystem_risk_probability.xml",
        "demo/mgmtsystem_risk_severity.xml",
    ],
    "installable": True,
}
