# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    event_immediate_id = fields.One2many("mgmtsystem.event", "immediate_action_id")
    event_ids = fields.Many2many(
        "mgmtsystem.event",
        "mgmtsystem_event_action_rel",
        "action_id",
        "event_id",
        "Events",
    )
