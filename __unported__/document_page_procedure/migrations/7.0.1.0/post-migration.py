# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

import logging
logger = logging.getLogger('upgrade')

def logged_query(cr, query, args=None):
    if args is None:
        args = []
    res = cr.execute(query, args)
    logger.debug('Running %s', query % tuple(args))
    logger.debug('%s rows affected', cr.rowcount)
    return cr.rowcount


def post_migrate_category(cr, version, category):
    logged_query(cr, """\
UPDATE document_page
SET parent_id = (SELECT id FROM document_page
                 WHERE name = %s AND type = 'category'
                 ORDER BY id DESC
                 LIMIT 1),
    name = name || ' (' || %s || ')'
WHERE parent_id = (SELECT id FROM document_page
                   WHERE name = %s AND type = 'category'
                   ORDER BY id ASC
                   LIMIT 1)
     AND type = 'content';""", (category, version, category))
    logged_query(cr, """\
UPDATE document_page
SET name = name || ' (' || %s || ')'
WHERE id = (SELECT id FROM document_page
            WHERE name = %s AND type = 'category'
            ORDER BY id ASC
            LIMIT 1)
     AND type = 'category';""", (version, category))


def migrate(cr, version):
    post_migrate_category(cr, version, 'Procedure')
    post_migrate_category(cr, version, 'Work Instructions')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
