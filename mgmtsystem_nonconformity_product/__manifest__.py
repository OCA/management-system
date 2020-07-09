# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name":     "Management System - Nonconformity Product",
    "summary":  "Bridge module between Product and Management System.",
    "version":  "12.0.1.0.0",
    "development_status": "Beta",

    "author":   "Associazione PNLUG - Gruppo Odoo, Odoo Community Association (OCA)",
    "website":  "https://gitlab.com/PNLUG/Odoo/management-system-improvements/tree/"
                "11.0/mgmtsystem_extended",
    "license":  "AGPL-3",

    "category": "Management System",
    "depends": [
        'product',
        'mgmtsystem_nonconformity',
        ],
    "data": [
        'views/mgmtsystem_nonconformity_views.xml',
        ],
    'installable': True,
}
