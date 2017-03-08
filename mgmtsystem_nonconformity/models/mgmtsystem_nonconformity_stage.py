# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis & Planing')),
    ('pending', _('Pending Approval')),
    ('open', _('In Progress')),
    ('review', _('In Review')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
]
_STATES_DICT = dict(_STATES)



class MgmtsystemNonconformityStage(models.Model):
    """This object is used to defined different state for non conformity."""
    _name = 'mgmtsystem.nonconformity.stage'
    _description = "Nonconformity Stages"
    _order = 'sequence'


    def _get_mail_template_id_domain(self):
        return [('model', '=', 'mgmtsystem.nonconformity')]

    def _get_default_nonconformity_ids(self):
        default_nonconformity_id = self.env.context.get('default_nonconformity_id')
        return [default_nonconformity_id] if default_nonconformity_id else None

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res


    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order states. Lower is better.", default=1)
    state = fields.Selection(
        _STATES,
        'State',
        readonly=False,
        default="draft",
    )
    state_name = fields.Char(compute='_state_name', string='State Description',)
    description = fields.Text(translate=True)

    nonconformity_ids = fields.Many2many('mgmtsystem.nonconformity', 'nonconformity_stage_type_rel', 'stage_id', 'nonconformity_id', string='Nonconformities',
        default=_get_default_nonconformity_ids)
    legend_priority = fields.Char(
        string='Priority Management Explanation', translate=True,
        help='Explanation text to help users using the star and priority mechanism on stages or nonconformities that are in this stage.')
    legend_blocked = fields.Char(
        string='Kanban Blocked Explanation', translate=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the action or nonconformity is in that stage.')
    legend_done = fields.Char(
        string='Kanban Valid Explanation', translate=True,
        help='Override the default value displayed for the done state for kanban selection, when the action or nonconformity is in that stage.')
    legend_normal = fields.Char(
        string='Kanban Ongoing Explanation', translate=True,
        help='Override the default value displayed for the normal state for kanban selection, when the action or nonconformity is in that stage.')
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=lambda self: self._get_mail_template_id_domain(),
        help="If set an email will be sent to the responsible person when the Action or Nonconformity reaches this Stage.")
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    is_starting = fields.Boolean(string='Is starting Stage', help='select stis checkbox if this is the default stage for new nonconformities')
