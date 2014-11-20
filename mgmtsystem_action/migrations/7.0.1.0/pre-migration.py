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

<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
=======

>>>>>>> Ported mgmtsystem_action
def get_legacy_name(original_name):
    return 'legacy_' + ('_').join(
        map(str, release.version_info[0:2])) + '_' + original_name

<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
=======

>>>>>>> Ported mgmtsystem_action
def rename_columns(cr, column_spec):
    for table in column_spec.keys():
        for (old, new) in column_spec[table]:
            if new is None:
                new = get_legacy_name(old)
            logger.info("table %s, column %s: renaming to %s",
                        table, old, new)
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
            cr.execute('ALTER TABLE "%s" RENAME "%s" TO "%s"' % (table, old, new,))
            cr.execute('DROP INDEX IF EXISTS "%s_%s_index"' % (table, old))
=======
            cr.execute(
                'ALTER TABLE "%s" RENAME "%s" TO "%s"' %
                (table, old, new,)
            )
            cr.execute(
                'DROP INDEX IF EXISTS "%s_%s_index"' %
                (table, old)
            )
>>>>>>> Ported mgmtsystem_action


column_renames = {
    'mgmtsystem_action': [
        ('stage_id', None)
    ]
}


def migrate(cr, version):
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
    rename_columns(cr, column_renames)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
    if version is None:
        return
    rename_columns(cr, column_renames)
>>>>>>> Ported mgmtsystem_action
