# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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


def migrate_nonconformity_action_ids(cr, column_names):
    logged_query(cr,  """
        SELECT COUNT(*)
        FROM mgmtsystem_nonconformity_action_rel""")
    if cr.fetchone()[0] > 0:
        logger.warning(
            "Attempt to migrate nonconformity action IDs failed: migration was already done.")
        return
    logger.info(
        "Moving nonconformity/action relations to mgmtsystem_nonconformity_action_rel")
    logged_query(cr, """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'mgmtsystem_nonconformity'""")
    action_fields = ['preventive_action_id', 'immediate_action_id', 'corrective_action_id']
    available_fields = [i for i in action_fields if i in column_names]
    for action_field in available_fields:
        logged_query(cr,  """
            INSERT INTO mgmtsystem_nonconformity_action_rel (nonconformity_id, action_id)
            (SELECT id, %s action_id FROM mgmtsystem_nonconformity
             WHERE %s IS NOT NULL);""" % (action_field, action_field))


def concatenate_action_comments(cr, column_names):
    logger.info("Concatenating action comments into evaluation_comments")
    action_fields = ['effectiveness_preventive', 'effectiveness_immediate', 'effectiveness_corrective']
    concatenation = " || ' ' || ".join([i for i in action_fields if i in column_names])
    if concatenation:
        logged_query(cr,  """
            UPDATE mgmtsystem_nonconformity
            SET evaluation_comments = %s
            WHERE evaluation_comments IS NULL;""" % concatenation)


def update_state_flags(cr):
    logger.info("Updating state flags")
    for i in [('open', 'o'), ('done', 'c')]:
        logged_query(cr,  """
            UPDATE mgmtsystem_nonconformity
            SET state = %s
            WHERE state = %s;""", i)


def migrate(cr, version):
    logged_query(cr, """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'mgmtsystem_nonconformity'""")
    column_names = (i[0] for i in cr.fetchall())
    migrate_nonconformity_action_ids(cr, column_names)
    concatenate_action_comments(cr, column_names)
    update_state_flags(cr)
