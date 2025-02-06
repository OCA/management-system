# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models, SUPERUSER_ID


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    def _get_default_project(self):
        if self.system_id and self.system_id.project_id:
            return self.system_id.project_id.id
        else:
            return False

    project_id = fields.Many2one("project.project", string="Project", default=_get_default_project)
    task_id = fields.Many2one("project.task", string="Task")

    def _get_closing_fase(self):
        closing_fase = self.env['mgmtsystem.action.stage'].search([('is_ending', '=', True)], limit=1)
        if not closing_fase:
            closing_fase = self.env['mgmtsystem.action.stage'].search([('fold', '=', True)], limit=1)
        return closing_fase or False

    def action_create_task(self):
        """
        Create a project task based on the current management system action.

        This method creates a new project task associated with the current management system action.
        It sets up the task with details from the action, including project, name, description, tags,
        and deadline. It also updates the action's stage and links the newly created task to the action.

        The method performs several checks before creating the task:
        - Ensures that the project tag and ending stage are properly set up.
        - Verifies that a task doesn't already exist for this action.
        - Checks that a project is set for the action.

        After creating the task, it posts messages to both the action and the task to log the creation.

        :raises UserError: If the project tag or stage is not known, if a task already exists,
                           or if no project is set.

        :return: None
        """
        self.ensure_one()
        ending_stage = self.env.ref('mgmtsystem_action_project.mgmtsystem_stage_task')
        tag = self.env['ir.model.data'].sudo()._xmlid_to_res_id(
            'mgmtsystem_action_project.mgmtsystem_action_proj_tag'
        )
        if not tag or not ending_stage:
            raise exceptions.UserError(_("Project tag or stage not known. please update module"))
        if self.task_id:
            raise exceptions.UserError(_("Task already exists"))
        elif not self.project_id:
            raise exceptions.UserError(_("Project not set"))
        else:
            vals = {
                'project_id': self.project_id.id,
                'name': self.name,
                'description': self.description,
                'tag_ids': [(4, tag)],
                "mgmtsystem_action_id": self.id,
                'date_deadline': self.date_deadline or False,
            }
            user = self.user_id
            if user:
                vals.update({'user_ids': [(4, self.user_id.id)]})
            task_id = self.env["project.task"].create(vals)
            self.write({
                'stage_id': ending_stage.id,
                'task_id': task_id.id
            })
            poster = self.env.user._is_internal() and self.env.user.id or SUPERUSER_ID
            title = _("Project task")
            self.with_user(poster).message_post(
                body=_("%s has been created", task_id._get_html_link(title=title)),
            )
            task_id.with_user(poster).message_post_with_source(
                'mail.message_origin_link',
                render_values={'self': task_id, 'origin': self},
                subtype_xmlid='mail.mt_note',
            )
