# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
<<<<<<< 527c6fad67cafc24c1059a64d5dc6ef1d1bd3083
#    it under the terms of the GNU General Public License as
=======
#    it under the terms of the GNU Affero General Public License as
>>>>>>> Moved document_page_procedure to root folder for port
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
<<<<<<< 527c6fad67cafc24c1059a64d5dc6ef1d1bd3083
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
{
<<<<<<< d89947875475312a48ee3ca2c131b5fddc62199d
    "name" : "Procedures",
    "version" : "0.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
    "license" : "AGPL-3",
    "category" : "Generic Modules/Others",
=======
    "name": "Document Management - Wiki - Procedures",
    "version": "1.0",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
>>>>>>> [FIX] PEP8 compliance after running flake8
=======
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Document Management - Wiki - Procedures",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
<<<<<<< 8be13d08270133e4a2f1db7fdda9f940fe3b12aa
>>>>>>> Moved document_page_procedure to root folder for port
    "description": """Procedure Template
    """,
=======
>>>>>>> Migration of document_page_procedure to Odoo 9.0
    "depends": [
        'document_page_work_instruction'
    ],
    "data": [
        'data/document_page_procedure.xml',
        'views/document_page_procedure.xml',
    ],
<<<<<<< b8b2c5c5a717bf426e543efe6428d2961b847aad
    "demo": [],
<<<<<<< fa0d893058a192bc1d2169abaa9c491bc70939b1
<<<<<<< 527c6fad67cafc24c1059a64d5dc6ef1d1bd3083
    "installable": True,
=======
    'installable': False,
>>>>>>> Moved document_page_procedure to root folder for port
=======
=======
    "demo": [
        'demo/document_page_procedure.xml',
    ],
<<<<<<< 8be13d08270133e4a2f1db7fdda9f940fe3b12aa
<<<<<<< 0ca876f1776d2d3b9b73093ae412c476b6a4634c
>>>>>>> Review changes from PR#35
    'installable': True,
<<<<<<< c82318b1532b7dad2f426a18e47d3a5a7e02bfd9
>>>>>>> Simple fix nothing to change
    "certificate": ''
=======
>>>>>>> Removed certificate from __openerp__
=======
    'installable': False,
>>>>>>> [MIG] Make modules uninstallable
=======
    'installable': True,
>>>>>>> Migration of document_page_procedure to Odoo 9.0
}
