# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
#    This module copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
=======
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
>>>>>>> Moved mgmtsystem_nonconformity to root for port
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

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
def logged_query(cr, query, args=None):
    if args is None:
        args = []
    res = cr.execute(query, args)
=======

def logged_query(cr, query, args=None):
    if args is None:
        args = []
    cr.execute(query, args)
>>>>>>> Moved mgmtsystem_nonconformity to root for port
    logger.debug('Running %s', query % tuple(args))
    logger.debug('%s rows affected', cr.rowcount)
    return cr.rowcount


def migrate_nonconformity_action_ids(cr, column_names):
    logged_query(cr,  """
        SELECT COUNT(*)
        FROM mgmtsystem_nonconformity_action_rel""")
    if cr.fetchone()[0] > 0:
        logger.warning(
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
            "Attempt to migrate nonconformity action IDs failed: migration was already done.")
        return
    logger.info(
        "Moving nonconformity/action relations to mgmtsystem_nonconformity_action_rel")
=======
            "Attempt to migrate nonconformity action IDs failed: migration "
            "was already done.")
        return
    logger.info(
        "Moving nonconformity/action relations to "
        "mgmtsystem_nonconformity_action_rel")
>>>>>>> Moved mgmtsystem_nonconformity to root for port
    logged_query(cr, """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'mgmtsystem_nonconformity'""")
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
    action_fields = ['preventive_action_id', 'immediate_action_id', 'corrective_action_id']
    available_fields = [i for i in action_fields if i in column_names]
    for action_field in available_fields:
        logged_query(cr,  """
            INSERT INTO mgmtsystem_nonconformity_action_rel (nonconformity_id, action_id)
            (SELECT id, %s action_id FROM mgmtsystem_nonconformity
             WHERE %s IS NOT NULL);""" % (action_field, action_field))
=======
    action_fields = [
        'preventive_action_id',
        'immediate_action_id',
        'corrective_action_id',
    ]
    available_fields = [i for i in action_fields if i in column_names]
    for action_field in available_fields:
        logged_query(cr,  """
INSERT INTO mgmtsystem_nonconformity_action_rel (nonconformity_id, action_id)
(SELECT id, %s action_id FROM mgmtsystem_nonconformity
WHERE %s IS NOT NULL);""" % (action_field, action_field))
>>>>>>> Moved mgmtsystem_nonconformity to root for port


def concatenate_action_comments(cr, column_names):
    logger.info("Concatenating action comments into evaluation_comments")
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
    action_fields = ['effectiveness_preventive', 'effectiveness_immediate', 'effectiveness_corrective']
    concatenation = " || ' ' || ".join([i for i in action_fields if i in column_names])
=======
    action_fields = [
        'effectiveness_preventive',
        'effectiveness_immediate',
        'effectiveness_corrective',
    ]
    concatenation = " || ' ' || ".join([
        i for i in action_fields if i in column_names]
    )
>>>>>>> Moved mgmtsystem_nonconformity to root for port
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
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
<<<<<<< d1ae6c91b0f02e30eb83ceb60d42bbf891243ce1
<<<<<<< 44fdbb69bcd6ca9c8f04f08af740c84b8c036dc0
    logger.info("Migrating mgmtsystem_nonconformity from version %s", version)
    cr.execute("select count(*) from mgmtsystem_nonconformity_action_rel")
    rowcount = cr.fetchone()[0]
    if rowcount == 0:
        logger.info("Moving nonconformity/action relations to mgmtsystem_nonconformity_action_rel")
        for action_field in ('preventive_action_id', 'immediate_action_id', 'corrective_action_id'):
            cr.execute("insert into mgmtsystem_nonconformity_action_rel"
                       "(nonconformity_id, action_id) "
                       "(SELECT id, %s FROM "
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8
                       "mgmtsystem_nonconformity "
=======
                       " mgmtsystem_nonconformity "
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
                       "WHERE %s IS NOT NULL )" % (action_field, action_field))
    else:
        logger.warning("Attempt to migrate nonconformity action IDs failed: migration was already done.")

    logger.info("Concatening action comments into evaluation_comments")
    cr.execute("update mgmtsystem_nonconformity set evaluation_comments = "
               "effectiveness_preventive || ' ' || effectiveness_immediate || ' ' || effectiveness_corrective "
               "where evaluation_comments is null")

    logger.info("Updating state flags")
    cr.execute("update mgmtsystem_nonconformity set state = 'open' where state = 'o'")
    cr.execute("update mgmtsystem_nonconformity set state = 'done' where state = 'c'")

    logger.info("mgmtsystem_nonconformity update... done!")
=======
    openupgrade.logged_query(cr, """
=======
    logged_query(cr, """
>>>>>>> [FIX] Migration scripts no longer fully dependent on openupgrade
=======
    if version is None:
        return
    logged_query(cr, """
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'mgmtsystem_nonconformity'""")
    column_names = (i[0] for i in cr.fetchall())
    migrate_nonconformity_action_ids(cr, column_names)
    concatenate_action_comments(cr, column_names)
    update_state_flags(cr)
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
>>>>>>> [7.0.1.0 Migration scirpts] Added mgmtsystem_action. Made mgmtsystem_nonconformity system more robust.
=======
>>>>>>> Moved mgmtsystem_nonconformity to root for port
