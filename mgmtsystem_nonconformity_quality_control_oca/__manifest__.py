# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mgmtsystem Nonconformity Quality Control Oca",
    "summary": """
        Bridge module between Quality Control and Non Conformities""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "depends": [
        "mgmtsystem_nonconformity",
        "quality_control_oca",
    ],
    "data": [
        "views/qc_inspection.xml",
        "views/mgmtsystem_nonconformity.xml",
    ],
    "demo": [],
}
