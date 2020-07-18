# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)

{
    "name": "Management System - Action Template",
    "summary": "Add Template management for Actions.",
    "version": "13.0.1.1.0",
    "author": "Associazione PNLUG - Gruppo Odoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_action"],
    "data": [
        "security/ir.model.access.csv",
        "views/mgmtsystem_action_template.xml",
        "views/mgmtsystem_action_views.xml",
    ],
    "installable": True,
}
