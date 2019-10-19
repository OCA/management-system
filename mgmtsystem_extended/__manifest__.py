# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name":     "Management System - Extend",
    "summary":  "Add informations and functionalities to Nonconformity.",
    "version":  "11.0.1.0.0",
    "development_status" : "Beta",

    "author":   "Associazione PNLUG - Gruppo Odoo, Odoo Community Association (OCA)",

    "website":  "https://gitlab.com/PNLUG/Odoo/management-system-improvements/tree/"
                "11.0/mgmtsystem_extended",
    "license":  "AGPL-3",

    "category": "Management System",
    "depends": ['mail',
                'contacts',
                'mgmtsystem',
                'mgmtsystem_nonconformity',
                'mgmtsystem_action',
                'stock'
                ],
    "data":    ['views/mgmtsystem_nonconformity_views.xml',
                'views/mgmtsystem_action_views.xml',
                'views/stock_picking_views.xml',
                'data/mgmtsystem_nonconformity_mail_data.xml'
                ],
    'installable': True,
}
