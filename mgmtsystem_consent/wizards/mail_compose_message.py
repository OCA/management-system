# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.multi
    def send_mail(self, auto_commit=False):
        """Update consent state if needed."""
        if (self.env.context.get('default_model') == 'mgmtsystem.consent' and
                self.env.context.get('default_res_id') and
                self.env.context.get('mark_consent_sent')):
            consent = self.env['mgmtsystem.consent'].browse(
                self.env.context['default_res_id'])
            if consent.state == 'draft':
                consent.with_context(tracking_disable=True).state = 'sent'
        return super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit)
