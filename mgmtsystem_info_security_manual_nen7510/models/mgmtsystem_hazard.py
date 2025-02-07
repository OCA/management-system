# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class MgmtsystemHazard(models.Model):
    _inherit = "mgmtsystem.hazard"

    code = fields.Char(
        string='Number',
        required=True,
        readonly=True,
        default='/',
        copy=False
    )

    canvas_name = fields.Char(string='Canvas Name')

    linked_procecure_ids = fields.Many2many(
        "document.page",
        string="Linked Procedures"
    )

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('mgmtsystem.hazard') or '/'
        return super(MgmtsystemHazard, self).create(vals)
