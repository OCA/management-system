# © 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Health and Safety Management System",
    "version": "16.0.1.0.1",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        "mgmtsystem_manual",
        "mgmtsystem_audit",
        "document_page_health_safety_manual",
        "mgmtsystem_review",
        "mgmtsystem_hazard_risk",
    ],
    "data": ["data/health_safety.xml"],
    "installable": True,
    "application": False,
}
