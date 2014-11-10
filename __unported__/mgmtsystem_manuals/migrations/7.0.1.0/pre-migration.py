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
logger.setLevel(logging.DEBUG)

xmlid_renames = [
    ('document_page_quality_manual.wiki_group_quality_manual',
     'mgmtsystem_manuals.manuals'),
]


def logged_query(cr, query, args=None):
    """
    Logs query and affected rows at level DEBUG
    """
    if args is None:
        args = []
    cr.execute(query, args)
    logger.debug('Running %s', query % tuple(args))
    logger.debug('%s rows affected', cr.rowcount)
    return cr.rowcount


def rename_xmlids(cr, xmlids_spec):
    """
    Rename XML IDs. Typically called in the pre script.
    One usage example is when an ID changes module. In OpenERP 6 for example,
    a number of res_groups IDs moved to module base from other modules (
    although they were still being defined in their respective module).
    """
    for (old, new) in xmlids_spec:
        if not old.split('.') or not new.split('.'):
            logger.error(
                'Cannot rename XMLID %s to %s: need the module '
                'reference to be specified in the IDs' % (old, new))
        else:
            query = ("UPDATE ir_model_data SET module = %s, name = %s "
                     "WHERE module = %s and name = %s")
            logged_query(cr, query, tuple(new.split('.') + old.split('.')))


def migrate(cr, version):
    if version is None:
        return
    rename_xmlids(cr, xmlid_renames)
