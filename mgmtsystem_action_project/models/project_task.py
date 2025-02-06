# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class MgmtsystemSystem(models.Model):
    _inherit = "project.task"

    mgmtsystem_action_id = fields.Many2one("mgmtsystem.action", string="Management System Action")

    def action_open_mgmtsystem_action(self):
        self.ensure_one()
        if not self.mgmtsystem_action_id:
            raise exceptions.UserError(_("No Management System Action linked to this task."))

        return {
            'name': _('Management System Action'),
            'type': 'ir.actions.act_window',
            'res_model': 'mgmtsystem.action',
            'res_id': self.mgmtsystem_action_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

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

    def action_create_corr_action(self):
        self.ensure_one()
        ending_stage = self.env.ref('mgmtsystem_action.stage_close')
        if self.mgmtsystem_action_id:
            raise exceptions.UserError(_("Action already exists"))
        if not self.project_id:
            system = self.env['mgmtsystem.system'].search([('project_id', '=', self.project_id.id)], limit=1)
            if not system:
                system = self.env['mgmtsystem.system'].search([], limit=1)
                if not system:
                    raise exceptions.UserError(_("No Management System found"))
        else:
            vals = {
                'project_id': self.project_id.id,
                'task_id': self.id,
                'name': self.name,
                'description': self.description,
                'date_deadline': self.date_deadline or False,
            }
            user = self.user_ids
            if user:
                vals.update({'user_id': user[0].id})
            mgmtsystem_action_id = self.env["mgmtsystem.action"].create(vals)
            self.write({
                'stage_id': ending_stage.id,
                'mgmtsystem_action_id': mgmtsystem_action_id.id
            })
            poster = self.env.user._is_internal() and self.env.user.id or SUPERUSER_ID
            title = _("Management system Action")
            self.with_user(poster).message_post(
                body=_("%s has been created", mgmtsystem_action_id._get_html_link(title=title)),
            )
            mgmtsystem_action_id.with_user(poster).message_post_with_source(
                'mail.message_origin_link',
                render_values={'self': mgmtsystem_action_id, 'origin': self},
                subtype_xmlid='mail.mt_note',
            )

