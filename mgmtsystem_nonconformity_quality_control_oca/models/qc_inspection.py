# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class QcInspection(models.Model):

    _inherit = "qc.inspection"

    mgmtsystem_nonconformity_ids = fields.One2many(
        "mgmtsystem.nonconformity", "qc_inspection_id", string="Non-Conformities"
    )

    mgmtsystem_nonconformity_count = fields.Integer(
        compute="_compute_mgmtsystem_nonconformity_count", string="# Non-Conformities"
    )

    @api.depends("mgmtsystem_nonconformity_ids")
    def _compute_mgmtsystem_nonconformity_count(self):
        for rec in self:
            rec.mgmtsystem_nonconformity_count = len(rec.mgmtsystem_nonconformity_ids)
