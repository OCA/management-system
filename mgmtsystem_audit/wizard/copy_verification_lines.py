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

from openerp import fields, models, api


class CopyVerificationLines(models.TransientModel):
    """Copy Verification Lines."""
    _name = "copy.verification.lines"
    _description = "Copy Verification Lines"

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
                'seq': line.seq,
                'name': line.name,
                'audit_id': audit_id,
                'procedure_id': line.procedure_id.id,
                'is_conformed': False,
            })
        return {'type': 'ir.actions.act_window_close'}
