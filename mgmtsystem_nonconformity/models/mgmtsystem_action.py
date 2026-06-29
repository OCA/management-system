# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    nonconformity_immediate_id = fields.One2many(
        "mgmtsystem.nonconformity", "immediate_action_id", readonly=True
    )
    nonconformity_ids = fields.Many2many(
        "mgmtsystem.nonconformity",
        "mgmtsystem_nonconformity_action_rel",
        "action_id",
        "nonconformity_id",
        "Nonconformities",
        readonly=True,
    )
    nonconformity_count = fields.Integer(
        compute="_compute_nonconformity_count",
        string="Number of nonconformities",
    )

    @api.depends("nonconformity_ids")
    def _compute_nonconformity_count(self):
        for action in self:
            action.nonconformity_count = len(action.nonconformity_ids)

    def action_open_nonconformities(self):
        self.ensure_one()
        return {
            "name": _("Nonconformities"),
            "type": "ir.actions.act_window",
            "res_model": "mgmtsystem.nonconformity",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.nonconformity_ids.ids)],
        }
