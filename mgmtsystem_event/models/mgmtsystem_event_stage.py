# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemEventStage(models.Model):
    """This object is used to defined different state for Event."""

    _name = "mgmtsystem.event.stage"
    _description = "Event Stages"
    _order = "sequence"

    def _get_states(self):
        return [
            ("draft", self.env._("Draft")),
            ("analysis", self.env._("Analysis")),
            ("pending", self.env._("Action Plan")),
            ("open", self.env._("In Progress")),
            ("done", self.env._("Closed")),
            ("cancel", self.env._("Cancelled")),
        ]

    name = fields.Char("Stage Name", required=True, translate=True)
    sequence = fields.Integer(
        help="Used to order states. Lower is better.", default=100
    )
    state = fields.Selection(selection=_get_states, default="draft")
    is_starting = fields.Boolean(
        string="Is starting Stage",
        help="select stis checkbox if this is the default stage \n" "for new events",
    )
    fold = fields.Boolean(
        string="Folded in Kanban",
        help="This stage is folded in the kanban view when there are \n"
        "no records in that stage to display.",
    )
