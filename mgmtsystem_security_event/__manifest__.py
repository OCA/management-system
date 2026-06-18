# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Feared Events",
    "version": "19.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management Systems",
    "depends": [
        "mgmtsystem",
        "document_page",
        "mgmtsystem_hazard",
    ],
    "data": [
        "data/document_page.xml",
        "data/mgmtsystem_risk_matrix_level.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/mgmtsystem_security_asset_category.xml",
        "views/mgmtsystem_security_asset_primary.xml",
        "views/mgmtsystem_security_asset_supporting.xml",
        "views/mgmtsystem_security_event.xml",
        "views/mgmtsystem_security_event_control.xml",
        "views/mgmtsystem_security_event_scenario.xml",
        "views/mgmtsystem_security_control.xml",
        "views/mgmtsystem_security_threat_source.xml",
        "views/mgmtsystem_security_vector.xml",
        "views/mgmtsystem_risk_matrix.xml",
        "views/mgmtsystem_risk_matrix_level.xml",
        "report/report.xml",
        "report/report_risk_matrix.xml",
    ],
    "demo": ["demo/mgmtsystem_security_event.xml"],
    "installable": True,
}
