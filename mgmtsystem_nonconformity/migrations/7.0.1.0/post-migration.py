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


def migrate(cr, version):
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
