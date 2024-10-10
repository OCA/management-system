# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models
from odoo.tools.misc import frozendict


class MgmtsystemNonconformityAbstract(models.AbstractModel):
    # TODO: Remove this on 17.0 and move everything on mail.thread
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
        for record in self:
            record.non_conformity_count = len(record.non_conformity_ids)

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


class MailThread(models.AbstractModel):
    _name = "mail.thread"
    _inherit = ["mail.thread", "mgmtsystem.nonconformity.abstract"]

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form" and self.env.user.has_group(
            "mgmtsystem.group_mgmtsystem_viewer"
        ):
            View = self.env["ir.ui.view"]
            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            doc = etree.XML(res["arch"])

            # We need to copy, because it is a frozen dict
            all_models = res["models"].copy()
            for node in doc.xpath("/form/div[hasclass('oe_chatter')]"):
                # _add_tier_validation_label process
                new_node = etree.fromstring(
                    "<field name='non_conformity_count' invisible='1'/>"
                )
                new_arch, new_models = View.postprocess_and_fields(new_node, self._name)
                new_node = etree.fromstring(new_arch)
                for model in list(filter(lambda x: x not in all_models, new_models)):
                    if model not in res["models"]:
                        all_models[model] = new_models[model]
                    else:
                        all_models[model] = res["models"][model]
                node.addprevious(new_node)
            res["arch"] = etree.tostring(doc)
            res["models"] = frozendict(all_models)
        return res

    @api.model
    def _get_view_fields(self, view_type, models):
        """
        We need to add this in order to fix the usage of form opening from
        trees inside a form
        """
        result = super()._get_view_fields(view_type, models)
        if view_type == "form" and self.env.user.has_group(
            "mgmtsystem.group_mgmtsystem_viewer"
        ):
            result[self._name].add("non_conformity_count")
        return result
