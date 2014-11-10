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

from openerp import release
import logging
logger = logging.getLogger('upgrade')


def get_legacy_name(original_name):
    return 'legacy_' + ('_').join(
        map(str, release.version_info[0:2])) + '_' + original_name


def logged_query(cr, query, args=None):
    if args is None:
        args = []
    cr.execute(query, args)
    logger.debug('Running %s', query % tuple(args))
    logger.debug('%s rows affected', cr.rowcount)
    return cr.rowcount


def migrate_stage_id(cr):
    stage_states = [
        ('draft', 'New'),
        ("open", "Accepted as Claim"),
        ("open", "Actions Defined"),
        ("open", "Qualification"),
        ("open", "Proposition"),
        ("open", "Negotiation"),
        ("done", "Actions Done"),
        ("done", "Won"),
        ("done", "Dead"),
        ("cancel", "Won't fix"),
        ("cancel", "Lost"),
    ]
    logged_query(cr, """
        UPDATE mgmtsystem_action
        SET stage_id = NULL""")
    legacy_stage_name = get_legacy_name("stage_id")
    # Check if the column exists
    logged_query(cr, """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'mgmtsystem_action'
          AND column_name = %s""", [legacy_stage_name])
    if not cr.fetchall():
        return
    query = """
        UPDATE mgmtsystem_action
        SET stage_id = (SELECT id
                        FROM crm_claim_stage
                        WHERE state = %%s
                        LIMIT 1)
        WHERE %s IN (SELECT id
                     FROM crm_case_stage
                     WHERE name = %%s)""" % legacy_stage_name
    for i in stage_states:
        logged_query(cr, query, i)


def migrate(cr, version):
    migrate_stage_id(cr)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
