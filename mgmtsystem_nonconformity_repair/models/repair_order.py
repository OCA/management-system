# Copyright 2020 - TODAY, Marcel Savegngo - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    mgmtsystem_nonconformity_ids = fields.One2many(
        "mgmtsystem.nonconformity", "repair_order_id", string="Non-Conformities"
    )

    mgmtsystem_nonconformity_count = fields.Integer(
        compute="_compute_mgmtsystem_nonconformity_count", string="# Non-Conformities"
    )

    @api.depends("mgmtsystem_nonconformity_ids")
    def _compute_mgmtsystem_nonconformity_count(self):
        for rec in self:
            rec.mgmtsystem_nonconformity_count = len(rec.mgmtsystem_nonconformity_ids)
