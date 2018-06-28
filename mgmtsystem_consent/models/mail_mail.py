# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def send_get_mail_body(self, partner=None):
        """Replace consent magic links.

        This replacement is done here instead of directly writing it into
        the ``mail.template`` to avoid writing the tokeinzed URL
        in the mail thread for the ``mgmtsystem.consent`` record,
        which would enable any reader of such thread to impersonate the
        subject and choose in its behalf.
        """
        result = super(MailMail, self).send_get_mail_body(partner=partner)
        # Avoid polluting other model mails
        if self.env.context.get("active_model") != "mgmtsystem.consent":
            return result
        # Tokenize consent links
        consent = self.env["mgmtsystem.consent"] \
            .browse(self.mail_message_id.res_id) \
            .with_prefetch(self._prefetch)
        result = result.replace("/consent/accept/", consent._url(True))
        result = result.replace("/consent/reject/", consent._url(False))
        return result
