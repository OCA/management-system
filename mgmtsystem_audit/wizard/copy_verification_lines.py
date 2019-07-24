# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


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
