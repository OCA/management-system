# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hazard",
    "version": "19.0.2.0.0",
    "author": "Savoir-faire Linux, Gray Matter Logic, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management Systems",
    "depends": ["mgmtsystem", "hr", "mgmtsystem_risk"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_hazard_security.xml",
        "views/mgmtsystem_hazard.xml",
        "views/mgmtsystem_hazard_origin.xml",
        "views/mgmtsystem_hazard_type.xml",
        "views/mgmtsystem_hazard_usage.xml",
        "views/mgmtsystem_hazard_control_measure.xml",
        "views/mgmtsystem_hazard_test.xml",
    ],
    "demo": [
        "demo/mgmtsystem_hazard_hazard.xml",
        "demo/mgmtsystem_hazard_origin.xml",
        "demo/mgmtsystem_hazard_type.xml",
        "demo/mgmtsystem_hazard_usage.xml",
    ],
    "installable": True,
}
