# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Hazard Risk",
    "version": "16.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_hazard", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_hazard_security.xml",
        "data/mgmtsystem_hazard_risk_computation.xml",
        "data/mgmtsystem_hazard_risk_type.xml",
        "views/mgmtsystem_hazard.xml",
        "views/mgmtsystem_hazard_risk_type.xml",
        "views/mgmtsystem_hazard_risk_computation.xml",
        "views/mgmtsystem_hazard_residual_risk.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
