# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - present Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api
import pdb
import re
import logging

_logger = logging.getLogger(__name__)


class MgmtsystemActionStage(models.Model):

    _name = 'mgmtsystem.action.stage'
    _description = "Action Stage"
    _order = 'sequence'

    def _get_mail_template_id_domain(self):
        return [('model', '=', 'mgmtsystem.action')]

    def _get_default_action_ids(self):
        default_action_id = self.env.context.get('default_action_id')
        return [default_action_id] if default_action_id else None

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

    name = fields.Char(string='Stage Name', required=True, translate=True)
    case_default = fields.Boolean('Common to All Teams')
    is_starting = fields.Boolean('Starting stage')
    is_ending = fields.Boolean('Ending stage')
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.")
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    #action_ids = fields.One2many('mgmtsystem.action', 'stage_id', string='Actions',
                               #domain=['|', ('stage_id.fold', '=', False), ('stage_id', '=', False)])
    action_ids = fields.Many2many('mgmtsystem.action', 'action_stage_type_rel', 'stage_id', 'action_id', string='Actions',
        default=_get_default_action_ids)
    color = fields.Integer(string='Color Index')
    
    legend_priority = fields.Char(
        string='Priority Management Explanation', translate=True,
        help='Explanation text to help users using the star and priority mechanism on stages or issues that are in this stage.')
    legend_blocked = fields.Char(
        string='Kanban Blocked Explanation', translate=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    legend_done = fields.Char(
        string='Kanban Valid Explanation', translate=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    legend_normal = fields.Char(
        string='Kanban Ongoing Explanation', translate=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=lambda self: self._get_mail_template_id_domain(),
        help="If set an email will be sent to the customer when the task or issue reaches this step.")
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
