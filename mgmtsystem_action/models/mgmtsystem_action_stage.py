# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtSystemActionStage(models.Model):
    _name = "mgmtsystem.action.stage"
    _description = "Action Stage"
    _order = "sequence, id"

    name = fields.Char("Stage Name", required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=100)
    fold = fields.Boolean(
        "Folded in Kanban",
        help="This stage is folded in the kanban view when there are "
        "no records in that stage to display.",
    )
    is_starting = fields.Boolean("Starting stage")
    is_ending = fields.Boolean("Ending stage")
