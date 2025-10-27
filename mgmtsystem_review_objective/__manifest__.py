# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mgmtsystem Review Objective",
    "summary": """Integrate reviews and objectives""",
    "version": "18.0.1.0.1",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "depends": [
        "mgmtsystem_review",
        "mgmtsystem_objective",
    ],
    "data": [
        "views/mgmtsystem_indicator_value.xml",
        "views/mgmtsystem_review.xml",
    ],
    "demo": [],
}
