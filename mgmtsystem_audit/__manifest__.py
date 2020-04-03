# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Management System - Audit",
    "version": "13.0.1.1.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_nonconformity", "base_automation"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_audit_security.xml",
        "data/audit_sequence.xml",
        "data/audit_automated_actions.xml",
        "views/mgmtsystem_audit.xml",
        "views/res_users.xml",
        "report/audit.xml",
        "report/verification.xml",
        "report/report.xml",
        "report/mgmtsystem_audit_pivot.xml",
        "wizard/copy_verification_lines.xml",
    ],
    "demo": ["demo/demo_audit.xml"],
    "installable": True,
}
