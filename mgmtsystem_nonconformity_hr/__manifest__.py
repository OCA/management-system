# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Nonconformity HR",
    "summary": "Bridge module between hr and mgmsystem and",
    "version": "13.0.1.0.0",
    "author": "Associazione PNLUG - Gruppo Odoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["hr", "mgmtsystem_nonconformity"],
    "data": ["views/mgmtsystem_nonconformity_views.xml"],
    "application": False,
    "installable": True,
    "auto_install": True,
}
