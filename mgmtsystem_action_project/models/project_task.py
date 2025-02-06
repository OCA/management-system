# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class MgmtsystemSystem(models.Model):
    _inherit = "project.task"

    mgmtsystem_action_id = fields.Many2one("mgmtsystem.action", string="Management System Action")

    @api.onchange("stage_id")
    def _onchange_mgmtsystem_stage_id(self):
        """ Also Change the state of the action when linked """
        if self.stage_id and self.mgmtsystem_action_id:
            if self.stage_id.fold:
                close_stage = self.mgmtsystem_action_id._get_closing_fase()
                if close_stage:
                    self.mgmtsystem_action_id.write({'stage_id': close_stage.id})
                    message = _("Action stage was closed because the linked task was set in closed stage")
                    self.mgmtsystem_action_id.message_post(body=message)
