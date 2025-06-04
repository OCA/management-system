# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mgmgtsystem Action Hazard",
    "summary": """Get access to actions related to a hazard""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "depends": [
        "mgmtsystem_action",
        "mgmtsystem_hazard",
    ],
    "data": [
        "views/mgmtsystem_action.xml",
        "views/mgmtsystem_hazard.xml",
    ],
    "demo": [],
    "auto_install": True,
}
