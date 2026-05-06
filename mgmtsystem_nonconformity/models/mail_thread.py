# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _get_non_conformities_domain(self):
        return [("res_model", "=", self._name), ("res_id", "=", self.id)]

    def _get_non_conformities_context(self):
        return {}

    def action_view_non_conformities(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_list"
        )
        action["domain"] = self._get_non_conformities_domain()
        action["context"] = self._get_non_conformities_context()
        return action

    def _get_mail_thread_data(self, request_list):
        res = super()._get_mail_thread_data(request_list)
        if self.env.user.has_group("mgmtsystem.group_mgmtsystem_viewer"):
            nonconformity_count = self.env["mgmtsystem.nonconformity"].search_count(
                [
                    ("res_model", "=", self._name),
                    ("res_id", "in", self.ids),
                ]
            )
            res["non_conformity_count"] = nonconformity_count
        return res
