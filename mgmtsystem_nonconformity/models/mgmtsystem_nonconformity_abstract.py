# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MgmtsystemNonconformityAbstract(models.AbstractModel):

    _name = "mgmtsystem.nonconformity.abstract"
    _description = "Nonconformity Abstract"

    non_conformity_ids = fields.One2many(
        "mgmtsystem.nonconformity",
        inverse_name="res_id",
        domain=lambda r: [("res_model", "=", r._name)],
        readonly=True,
    )

    non_conformity_count = fields.Integer(compute="_compute_non_conformity_count")

    @api.depends("non_conformity_ids")
    def _compute_non_conformity_count(self):
        self.ensure_one()
        self.non_conformity_count = len(self.non_conformity_ids)

    def _get_non_conformities_domain(self):
        return [("res_model", "=", self._name), ("res_id", "=", self.id)]

    def _get_non_conformities_context(self):
        return {}

    def action_view_non_conformities(self):
        self.ensure_one()
        action = self.env.ref(
            "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_list"
        ).read()[0]
        action["domain"] = self._get_non_conformities_domain()
        action["context"] = self._get_non_conformities_context()
        return action
