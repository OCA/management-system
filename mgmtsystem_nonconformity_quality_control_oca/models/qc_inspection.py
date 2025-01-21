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

    def action_view_nonconformities(self):
        action = self.env.ref(
            "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_list"
        ).read()[0]
        if self.mgmtsystem_nonconformity_count > 1:
            action["domain"] = [("id", "in", self.mgmtsystem_nonconformity_ids.ids)]
        else:
            action["views"] = [
                (
                    self.env.ref(
                        "mgmtsystem_nonconformity.view_mgmtsystem_nonconformity_form"
                    ).id,
                    "form",
                )
            ]
            action["res_id"] = (
                self.mgmtsystem_nonconformity_ids
                and self.mgmtsystem_nonconformity_ids.ids[0]
                or False
            )
            action["context"] = {
                "search_default_qc_inspection_id": self.id,
                "default_qc_inspection_id": self.id,
                "default_name": self.name,
                "default_company_id": self.company_id.id,
            }
        return action
