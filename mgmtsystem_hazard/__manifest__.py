# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hazard",
    "version": "13.0.1.1.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_hazard_security.xml",
        "views/mgmtsystem_hazard.xml",
        "views/mgmtsystem_hazard_origin.xml",
        "views/mgmtsystem_hazard_type.xml",
        "views/mgmtsystem_hazard_probability.xml",
        "views/mgmtsystem_hazard_severity.xml",
        "views/mgmtsystem_hazard_usage.xml",
        "views/mgmtsystem_hazard_control_measure.xml",
        "views/mgmtsystem_hazard_test.xml",
    ],
    "demo": [
        "demo/mgmtsystem_hazard_hazard.xml",
        "demo/mgmtsystem_hazard_origin.xml",
        "demo/mgmtsystem_hazard_probability.xml",
        "demo/mgmtsystem_hazard_severity.xml",
        "demo/mgmtsystem_hazard_type.xml",
        "demo/mgmtsystem_hazard_usage.xml",
    ],
    "installable": True,
}
