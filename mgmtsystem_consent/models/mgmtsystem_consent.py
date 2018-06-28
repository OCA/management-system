# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import hashlib
import hmac

from odoo import api, fields, models


class MgmtSystemConsent(models.Model):
    _name = 'mgmtsystem.consent'
    _description = "Consent of data processing"
    _inherit = "mail.thread"
    _rec_name = "partner_id"
    _sql_constraints = [
        ("unique_partner_system", "UNIQUE(partner_id, system_id)",
         "Duplicated partner in this management system"),
    ]

    active = fields.Boolean(
        default=True,
        index=True,
    )
    accepted = fields.Boolean(
        track_visibility=True,
        help="Indicates current acceptance status, which can come from "
             "subject's last answer, or from the default specified in the "
             "related management system.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Subject",
        required=True,
        readonly=True,
        track_visibility=True,
        help="Subject asked for consent.",
    )
    system_id = fields.Many2one(
        "mgmtsystem.system",
        "System",
        readonly=True,
        required=True,
        track_visibility=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Awaiting response"),
            ("answered", "Answered"),
        ],
        default="draft",
        readonly=True,
        required=True,
        track_visibility=True,
    )

    def _token(self):
        """Secret token to publicly authenticate this record."""
        secret = self.env["ir.config_parameter"].sudo().get_param(
            "database.secret")
        params = "{}-{}-{}-{}".format(
            self.env.cr.dbname,
            self.id,
            self.partner_id.id,
            self.system_id.id,
        )
        return hmac.new(
            secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha512,
        ).hexdigest()

    def _url(self, accept):
        """Tokenized absolute URL to let subject decide consent.

        :param bool accept:
            Indicates if you want the acceptance URL, or the rejection one.
        """
        return "/consent/{}/{}/{}?dbname={}".format(
            "accept" if accept else "reject",
            self.id,
            self._token(),
            self.env.cr.dbname,
        )

    def _send_consent_notification(self):
        """Send email notification to subject."""
        consents_by_template = {}
        for one in self.with_context(tpl_force_default_to=True,
                                     mail_notify_user_signature=False,
                                     mail_auto_subscribe_no_notify=True,
                                     mark_consent_sent=True):
            # Group consents by template, to send in batch where possible
            template_id = one.system_id.consent_template_id.id
            consents_by_template.setdefault(template_id, one)
            consents_by_template[template_id] |= one
        # Send emails
        for template_id, consents in consents_by_template.items():
            consents.message_post_with_template(
                template_id,
                # This mode always sends email, regardless of partner's
                # notification preferences; we use it here because it's very
                # likely that we are asking authorisation to send emails
                composition_mode="mass_mail",
            )

    def _run_action(self):
        """Execute server action defined in management system."""
        for one in self:
            # Always skip draft consents
            if one.state == "draft":
                continue
            action = one.system_id.server_action_id.with_context(
                active_id=one.id,
                active_model=one._name,
            )
            action.run()

    @api.model
    def create(self, vals):
        """Run server action on create."""
        result = super(MgmtSystemConsent, self).create(vals)
        # Sync the default acceptance status
        result.sudo()._run_action()
        return result

    def write(self, vals):
        """Run server action on update."""
        # We will check if all draft consents change
        changed = self.filtered(lambda one: one.state == "draft")
        if "accepted" in vals:
            # Also check those whose acceptance is going to change
            changed |= self.filtered(
                lambda one: one.accepted != vals["accepted"]
            )
        result = super(MgmtSystemConsent, self).write(vals)
        changed._run_action()
        return result

    def message_get_suggested_recipients(self):
        result = super(MgmtSystemConsent, self) \
            .message_get_suggested_recipients()
        reason = self._fields["partner_id"].string
        for one in self:
            one._message_add_suggested_recipient(
                result,
                partner=one.partner_id,
                reason=reason,
            )
        return result

    def action_manual_ask(self):
        """Let user manually ask for consent."""
        return {
            "context": {
                "default_composition_mode": "mass_mail",
                "default_model": self._name,
                "default_res_id": self.id,
                "default_template_id": self.system_id.consent_template_id.id,
                "default_use_template": True,
                "mark_consent_sent": True,
                "tpl_force_default_to": True,
            },
            "force_email": True,
            "res_model": "mail.compose.message",
            "target": "new",
            "type": "ir.actions.act_window",
            "view_mode": "form",
        }

    def action_auto_ask(self):
        """Automatically ask for consent."""
        templated = self.filtered("system_id.consent_template_id")
        automated = templated.filtered(
            lambda one: one.system_id.consent_required == "auto")
        automated._send_consent_notification()

    def action_answer(self, answer):
        """Process answer.

        :param bool answer:
            Did the subject accept?
        """
        self.write({"state": "answered", "accepted": answer})
        self._send_consent_notification()
