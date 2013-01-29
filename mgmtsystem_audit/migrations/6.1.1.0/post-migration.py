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
    logger.info("Migrating mgmtsystem_audit from version %s", version)

    logger.info("Updating state flags")
    cr.execute("update mgmtsystem_audit set state = 'open' where state = 'o'")
    cr.execute("update mgmtsystem_audit set state = 'done' where state = 'c'")

    logger.info("Renaming relation columns")
    # Our model's relation to nonconformity was previously wrongly defined as:
    # 'nonconformity_ids': fields.many2many('mgmtsystem.nonconformity','mgmtsystem_audit_nonconformity_rel','mgmtsystem_action_id','mgmtsystem_audit_id','Nonconformities')
    # In v1.0, it's been fixed to:
    # 'nonconformity_ids': fields.many2many('mgmtsystem.nonconformity','mgmtsystem_audit_nonconformity_rel','mgmtsystem_audit_id','mgmtsystem_nonconformity_id','Nonconformities')
    # However, OpenERP doesn't seem to automatically handle column renames here. We have to do it manually.

    # Now, verify if we actually have the old schema.
    cr.execute("select * from mgmtsystem_audit_nonconformity_rel limit 0")
    colnames = set(desc[0] for desc in cr.description)
    if "mgmtsystem_action_id" in colnames:
        # It's ok, we can proceed with the renames.
        cr.execute("alter table mgmtsystem_audit_nonconformity_rel rename column mgmtsystem_audit_id to mgmtsystem_nonconformity_id")
        cr.execute("alter table mgmtsystem_audit_nonconformity_rel rename column mgmtsystem_action_id to mgmtsystem_audit_id")
    else:
        logging.warning("mgmtsystem_audit_nonconformity_rel already migrated. Skipping.")

    logger.info("mgmtsystem_audit update... done!")
