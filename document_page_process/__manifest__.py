# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Document Page Process',
    'summary': """
        Add Process document page""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV, Odoo Community Association (OCA)',
    'website': 'https://www.acsone.eu',
    'depends': [
        'document_page',
        'mgmtsystem',
    ],
    'data': [
        'data/document_page_process.xml',
        'views/document_page_process.xml',
    ],
    'demo': [
    ],
}
