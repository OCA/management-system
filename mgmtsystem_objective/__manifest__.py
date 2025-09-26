# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mgmtsystem Objective",
    "summary": """Define objectives on your management system""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "depends": ["mgmtsystem", "mail", "uom"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/mgmtsystem_indicator_value.xml",
        "views/mgmtsystem_indicator.xml",
        "views/mgmtsystem_objective.xml",
    ],
    "demo": [
        "demo/mgmtsystem_objective.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mgmtsystem_objective/static/src/**/*.esm.js",
        ],
        "web.assets_unit_tests": [
            "mgmtsystem_objective/static/tests/**/*.test.js",
        ],
    },
}
