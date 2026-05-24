# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Management System - Event",
    "version": "18.0.0.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_action", "document_page_procedure"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_event_security.xml",
        "views/mgmtsystem_event.xml",
        "views/mgmtsystem_origin.xml",
        "views/mgmtsystem_cause.xml",
        "views/mgmtsystem_severity.xml",
        "views/mgmtsystem_action.xml",
        "views/mgmtsystem_event_stage.xml",
        "views/mgmtsystem_event_tag.xml",
        "data/sequence.xml",
        "data/mgmtsystem_event_severity.xml",
        "data/mgmtsystem_event_origin.xml",
        "data/mgmtsystem_event_cause.xml",
        "data/mgmtsystem_event_stage.xml",
        "data/mail_message_subtype.xml",
        "reports/mgmtsystem_event_report.xml",
    ],
    "demo": [
        "demo/mgmtsystem_event_origin.xml",
        "demo/mgmtsystem_event_cause.xml",
        "demo/mgmtsystem_event.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mgmtsystem_event/static/src/**/*.xml",
            "mgmtsystem_event/static/src/**/*.esm.js",
        ],
        "web.assets_unit_tests": [
            "mgmtsystem_event/static/tests/**/*",
        ],
    },
    "installable": True,
}
