# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class MgmtSystemSystem(models.Model):
    _inherit = 'mgmtsystem.system'

    server_action_id = fields.Many2one(
        "ir.actions.server",
        "Server action",
        domain=[
            ("model_id.model", "=", "mgmtsystem.consent"),
        ],
        help="Run this action when a new consent request is created or its "
             "acceptance status is updated.",
    )
    consent_ids = fields.One2many(
        "mgmtsystem.consent",
        "system_id",
        "Consents",
    )
    consent_ids_count = fields.Integer(
        "Consents",
        compute="_compute_consent_ids_count",
    )
    consent_required = fields.Selection(
        [("auto", "Automatically"), ("manual", "Manually")],
        "Ask subjects for consent",
        help="Enable if you need to track any kind of consent "
             "from the affected subjects",
    )
    consent_template_id = fields.Many2one(
        "mail.template",
        "Email template",
        default=lambda self: self._default_consent_template_id(),
        domain=[
            ("model", "=", "mgmtsystem.consent"),
        ],
        help="Email to be sent to subjects to ask for consent. "
             "A good template should include details about the current "
             "consent request status, how to change it, and where to "
             "get more information.",
    )
    default_consent = fields.Boolean(
        "Accepted by default",
        help="Should we assume the subject has accepted if we receive no "
             "response?",
    )
    subject_domain = fields.Char(
        "Subjects filter",
        default="[]",
        help="Selection filter to find specific subjects included.",
    )

    # Hidden helpers help user design new templates
    consent_template_default_body_html = fields.Text(
        compute="_compute_consent_template_defaults",
    )
    consent_template_default_subject = fields.Char(
        compute="_compute_consent_template_defaults",
    )

    @api.model
    def _default_consent_template_id(self):
        return self.env.ref("mgmtsystem_consent.consent_mail", False)

    @api.depends("consent_ids")
    def _compute_consent_ids_count(self):
        for one in self:
            one.consent_ids_count = len(one.consent_ids)

    def _compute_consent_template_defaults(self):
        """Used in context values, to help users design new templates."""
        template = self._default_consent_template_id()
        if template:
            self.update({
                "consent_template_default_body_html": template.body_html,
                "consent_template_default_subject": template.subject,
            })

    @api.constrains("consent_required", "consent_template_id")
    def _check_auto_consent_has_template(self):
        """Require a mail template to automate consent requests."""
        for one in self:
            if one.consent_required == "auto" and not one.consent_template_id:
                raise ValidationError(
                    _("Specify a mail template to ask automated consent."))

    @api.model
    def _cron_new_consents(self):
        """Ask all missing automatic consent requests."""
        automatic = self.search([("consent_required", "=", "auto")])
        automatic.action_new_consents()

    def action_new_consents(self):
        """Generate new consent requests."""
        consents = self.env["mgmtsystem.consent"]
        # Skip systems where consent is not required
        for one in self.with_context(active_test=False) \
                .filtered("consent_required"):
            domain = safe_eval(one.subject_domain)
            domain += [
                ("id", "not in", one.mapped("consent_ids.partner_id").ids),
            ]
            # Create missing consent requests
            for missing in self.env["res.partner"].search(domain):
                consents |= consents.create({
                    "partner_id": missing.id,
                    "accepted": one.default_consent,
                    "system_id": one.id,
                })
        # Send consent request emails for automatic systems
        consents.action_auto_ask()
        # Redirect user to new consent requests generated
        return {
            "domain": [("id", "in", consents.ids)],
            "name": _("Generated consents"),
            "res_model": consents._name,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
        }
