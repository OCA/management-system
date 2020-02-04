# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']
         
    def _compute_project_task_count(self):
        for mgmtsystem_action in self:
            mgmtsystem_action.project_count = len(mgmtsystem_action.project_task_ids)
    
    project_task_ids = fields.Many2many('project.task','mgmtsystem_action_project_task_rel','mgmtsystem_action_id','project_task_id','Project Task Ids')
    project_task_count = fields.Integer(compute='_compute_project_task_count', string="Number of project task")
    
class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['project.task']

    def _compute_mgmtsystem_action_count(self):
        for project_task in self:
            project_task.mgmtsystem_action_count = len(project_task.mgmtsystem_action_ids)
    
    mgmtsystem_action_ids = fields.Many2many('mgmtsystem.action','mgmtsystem_action_project_task_rel','project_task_id','mgmtsystem_action_id','Action Ids')
    mgmtsystem_action_count = fields.Integer(compute='_compute_mgmtsystem_action_count', string="Number of action")