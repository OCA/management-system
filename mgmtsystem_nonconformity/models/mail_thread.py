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

    def _thread_to_store(self, store: Store, /, *, request_list=None, **kwargs):
        result = super()._thread_to_store(store, request_list=request_list, **kwargs)
        if self.env.user.has_group("mgmtsystem.group_mgmtsystem_viewer"):
            nonconformity_count = {
                res_id: res_count
                for res_id, res_count in self.env[
                    "mgmtsystem.nonconformity"
                ]._read_group(
                    [
                        ("res_model", "=", self._name),
                        ("res_id", "in", self.ids),
                    ],
                    ["res_id"],
                    ["res_id:count"],
                )
            }
            for thread in self:
                store.add(
                    thread,
                    {"non_conformity_count": nonconformity_count.get(thread.id, 0)},
                    as_thread=True,
                )
        return result
