# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    def _compute_complete_name(self):
        for action in self:
            action.complete_name = self.name

    name = fields.Char('Claim Subject')
    action_type = fields.Selection([
        ('action', 'Action'),
        ('project', 'Project'),
        ],
        string='Action Type',
        required=True,
        default='action',
    )
    project_id = fields.Many2one('project.project', 'Project')
    complete_name = fields.Char('Complete Name', store=True,
                                compute='_compute_complete_name')
