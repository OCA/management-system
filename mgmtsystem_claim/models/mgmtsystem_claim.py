##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime, timedelta

from odoo import _, api, fields, models


class MgmtsystemClaim(models.Model):
    _name = "mgmtsystem.claim"
    _description = "Claim for Management System"
    _inherit = "crm.claim"

    reference = fields.Char("Reference", required=True, readonly=True, default="NEW")

    message_ids = fields.One2many(
        "mail.message", "res_id", "Messages", domain=[("model", "=", _name)]
    )

    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )

    stage_id = fields.Many2one(
        "mgmtsystem.claim.stage", "Stage", default=lambda self: self.get_default_stage()
    )

    @api.model
    def get_default_stage(self):
        return self.env["mgmtsystem.claim.stage"].search([])[0].id

    @api.model_create_multi
    def create(self, vals_list):
        for one_vals in vals_list:
            if one_vals.get("reference", _("New")) == _("New"):
                Sequence = self.env["ir.sequence"]
                one_vals["reference"] = Sequence.next_by_code("mgmtsystem.action")
        actions = super().create(vals_list)
        actions.send_mail_for_action()
        return actions

    def get_action_url(self):
        """Return action url to be used in email templates."""
        base_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("web.base.url", default="http://localhost:8069")
        )
        url = ("{}/web#db={}&id={}&model={}").format(
            base_url, self.env.cr.dbname, self.id, self._name
        )
        return url

    def send_mail_for_action(self, force_send=True):
        template = self.env.ref("mgmtsystem_claim.email_template_new_claim_reminder")
        for action in self:
            template.send_mail(action.id, force_send=force_send)
        return True

    @api.model
    def process_reminder_queue(self, reminder_days=10):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=reminder_days)
        stage_close = self.env.ref("mgmtsystem_claim.stage_close")
        actions = self.search(
            [("stage_id", "!=", stage_close.id), ("date_deadline", "=", cur_date)]
        )
        if actions:
            template = self.env.ref(
                "mgmtsystem_claim.email_template_remain_claim_reminder"
            )
            for action in actions:
                template.send_mail(action.id)
            return True
        return False
