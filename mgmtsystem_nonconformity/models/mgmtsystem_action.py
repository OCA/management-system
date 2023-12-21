# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    nonconformity_immediate_id = fields.One2many(
        "mgmtsystem.nonconformity", "immediate_action_id", readonly=True
    )
    nonconformity_ids = fields.Many2many(
        "mgmtsystem.nonconformity",
        "mgmtsystem_nonconformity_action_rel",
        "action_id",
        "nonconformity_id",
        "Nonconformities",
        readonly=True,
    )
