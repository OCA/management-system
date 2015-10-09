# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Quality Manual',
    'version': '8.0.1.0.0',
    'category': 'Management System',
    'complexity': "easy",
    'description': """
Quality Manual
==============

This module provides a quality manual template with the same structure
as the ISO 9001 standard.

Contributors
------------

 * Odoo SA <info@odoo.com>
 * Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
    """,
    'author': "OpenERP SA,Odoo Community Association (OCA)",
    'website': 'http://openerp.com',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem_manuals'
    ],
    'data': [
        'data/document_page_data.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': [
        'images/wiki_pages_quality_manual.jpeg'
    ],
}
