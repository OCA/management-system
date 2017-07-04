# -*- coding: utf-8 -*-
from odoo import api, models, fields


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    def _compute_complete_name(self):
        for action in self:
            action.complete_name = '%s %s' % action.name_get()[0]

    name = fields.Char('Claim Subject', size=128)
    action_type = fields.Selection([
        ('action', 'Action'),
        ('project', 'Project'),
    ],
        string='Action Type',
        required=True,
        default='action',
    )
    project_id = fields.Many2one('project.project', 'Project')
    complete_name = fields.Char('Complete Name',
                                compute='_compute_complete_name',
                                size=250, store=True)

    @api.multi
    def name_get(self):
        res = list()
        for o in self:
            r = (o.id, o.name)
            if o.action_type == 'project' and o.project_id:
                r = (o.id, o.project_id.name)
            res.append(r)
        return res
