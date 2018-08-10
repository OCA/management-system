############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2016 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
#    planned by: Sabrina Romero <sabrina@vauxoo.com>
############################################################################
{
    "name": "Management Nonconformity Report",
    "version": "11.0.1.0.0",
    "author": "Vauxoo,Odoo Community Association (OCA)",
    "website": "https://www.vauxoo.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        "web",
        "mgmtsystem_nonconformity"
    ],
    "data": [
        "data/report_paperformat.xml",
        "view/layout.xml",
        "view/report_nonconformity.xml",
    ],
    "demo": [],
    "installable": True,
}
