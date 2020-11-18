# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemActionTemplate(models.Model):

    _name = 'mgmtsystem.action.template'
    _description = 'Extend actions adding fields and method for template management'

    def _selection_type_action(self):
        return self.env['mgmtsystem.action']._fields['type_action'].selection

    name = fields.Char(required=True)
    description = fields.Html()
    type_action = fields.Selection(
        selection=lambda self: self._selection_type_action(),
        string='Response Type'
    )
    user_id = fields.Many2one(
        'res.users',
        'Responsible',
        default=lambda self: self.env['mgmtsystem.action']._default_owner(),
        required=True
    )
    tag_ids = fields.Many2many('mgmtsystem.action.tag', string='Tags')
