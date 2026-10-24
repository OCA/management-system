# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.mail.tools.discuss import Store


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

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

    def _store_thread_fields(self, res: Store.FieldList, *, request_list, **kwargs):
        result = super()._store_thread_fields(res, request_list=request_list, **kwargs)
        if request_list:
            if self.env.user.has_group("mgmtsystem.group_mgmtsystem_viewer"):
                counts = dict(
                    self.env["mgmtsystem.nonconformity"]._read_group(
                        [("res_model", "=", self._name), ("res_id", "in", self.ids)],
                        ["res_id"],
                        ["__count"],
                    )
                )
            else:
                counts = {}
            res.attr("non_conformity_count", lambda thread: counts.get(thread.id, 0))
        return result
