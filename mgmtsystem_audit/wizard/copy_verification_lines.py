# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from osv import fields, osv


class copy_verification_lines(osv.osv_memory):
    """
    Copy Verification Lines
    """
    _name = "copy.verification.lines"
    _description = "Copy Verification Lines"
    _columns = {
        'audit_src': fields.many2one('mgmtsystem.audit', 'Choose audit'),
    }

    def copy(self, cr, uid, ids, context=None):
        # Code to copy verification lines from the chosen audit to the current one
        if context is None:
            context = {}

        audit_proxy = self.pool.get(context.get('active_model'))
        verification_line_proxy = self.pool.get('mgmtsystem.verification.line')
        src_id = self.read(cr, uid, ids, [], context=context)[0]['audit_src'][0]

        for line in audit_proxy.browse(cr, uid, src_id, context=context).line_ids:
            verification_line_proxy.create(cr, uid, {
                'seq': line.seq,
                'name': line.name,
                'audit_id': context['active_id'],
                'procedure_id': line.procedure_id.id,
                'is_conformed': False,
            }, context=context)
        return {'type': 'ir.actions.act_window_close'}

copy_verification_lines()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
