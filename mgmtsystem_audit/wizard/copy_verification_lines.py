# -*- coding: utf-8 -*-
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

<<<<<<< e00fa43c595690d36669b683a085e5741efb9324
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201
from osv import fields, osv


class copy_verification_lines(osv.osv_memory):
=======
from openerp.osv import fields, orm


class copy_verification_lines(orm.TransientModel):
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
    """
    Copy Verification Lines
    """
=======
from openerp import fields, models, api


class CopyVerificationLines(models.TransientModel):
    """Copy Verification Lines."""
>>>>>>> [MIG] mgmtsystem_audit
    _name = "copy.verification.lines"
    _description = "Copy Verification Lines"

<<<<<<< e00fa43c595690d36669b683a085e5741efb9324
    def copy(self, cr, uid, ids, context=None):
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201
        # Code to copy verification lines from the chosen audit to the current one
=======
        # Copy verification lines from the chosen audit to the current one
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
        if context is None:
            context = {}

        audit_proxy = self.pool.get(context.get('active_model'))
        verification_line_proxy = self.pool.get('mgmtsystem.verification.line')
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201
        src_id = self.read(cr, uid, ids, [], context=context)[0]['audit_src'][0]

        for line in audit_proxy.browse(cr, uid, src_id, context=context).line_ids:
=======
        src_id = self.read(
            cr, uid, ids, ['audit_src'], context=context)[0]['audit_src'][0]

        for line in audit_proxy.browse(
                cr, uid, src_id, context=context).line_ids:
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
            verification_line_proxy.create(cr, uid, {
=======
    audit_src = fields.Many2one('mgmtsystem.audit', 'Choose audit')

    @api.multi
    def copyVerificationLines(self):
        # Copy verification lines from the chosen audit to the current one
        audit_proxy = self.env[self._context.get('active_model')]
        verification_line_proxy = self.env['mgmtsystem.verification.line']
        audit_id = self._context.get('active_id')
        src_id = self.read(['audit_src'])[0]['audit_src'][0]
        for line in audit_proxy.browse(src_id).line_ids:
            verification_line_proxy.create({
>>>>>>> [MIG] mgmtsystem_audit
                'seq': line.seq,
                'name': line.name,
                'audit_id': audit_id,
                'procedure_id': line.procedure_id.id,
                'is_conformed': False,
            })
        return {'type': 'ir.actions.act_window_close'}
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201

copy_verification_lines()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
