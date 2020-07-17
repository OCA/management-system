# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)

{
    "name":     "Management System - Nonconformity Type",
    "summary":  "Add Nonconformity classification for the root context.",
    "version":  "12.0.1.0.0",
    "development_status" : "Beta",
    "author":   "Associazione PNLUG - Gruppo Odoo, Odoo Community Association (OCA)",
    "website":  "https://github.com/OCA/management-system",
    "license":  "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem',
                'mgmtsystem_nonconformity',
                'mgmtsystem_partner',
                ],
    "data":    ['views/mgmtsystem_nonconformity_views.xml',
                'data/mgmtsystem_nonconformity_mail_data.xml'
                ],
    'installable': True,
}
