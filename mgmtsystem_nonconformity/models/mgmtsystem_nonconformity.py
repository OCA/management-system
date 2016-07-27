# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, api, fields


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _rec_name = "description"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = "create_date desc"
    _track = {
        'field': {
            'mgmtsystem_nonconformity.subtype_analysis': (
                lambda s, o: o["state"] == "analysis"
            ),
            'mgmtsystem_nonconformity.subtype_pending': (
                lambda s, o: o["state"] == "pending"
            ),
        },
    }

    def _default_stage(self):
        """Return the default stage."""
        return self.env.ref('mgmtsystem_nonconformity.stage_draft')

    @api.model
    def _stage_groups(self, present_ids, domain, **kwargs):
        """This method is used by Kanban view to show empty stages."""
        # perform search
        # We search here stage objects
        result = self.env[
            'mgmtsystem.nonconformity.stage'].search([]).name_get()
        return result, None

    _group_by_full = {
        'stage_id': _stage_groups
    }

    # 1. Description
    name = fields.Char('Name')
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )
    # Compute data
    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True, default=1)
    days_since_updated = fields.Integer(
        readonly=True,
        compute='_compute_days_since_updated',
        store=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close',
        compute='_compute_number_of_days_to_close',
        store=True,
        readonly=True)
    closing_date = fields.Datetime('Closing Date', readonly=True)

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    reference = fields.Char('Related to')
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
        track_visibility=True,
    )
    manager_user_id = fields.Many2one(
        'res.users',
        'Manager',
        required=True,
        track_visibility=True,
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user.id,
        track_visibility=True,
    )
    origin_ids = fields.Many2many(
        'mgmtsystem.nonconformity.origin',
        'mgmtsystem_nonconformity_origin_rel',
        'nonconformity_id',
        'origin_id',
        'Origin',
        required=True,
    )
    procedure_ids = fields.Many2many(
        'document.page',
        'mgmtsystem_nonconformity_procedure_rel',
        'nonconformity_id',
        'procedure_id',
        'Procedure',
    )
    description = fields.Text('Description', required=True)
    system_id = fields.Many2one('mgmtsystem.system', 'System')
    stage_id = fields.Many2one(
        'mgmtsystem.nonconformity.stage',
        'Stage',
        track_visibility=True,
        copy=False,
        default=_default_stage)
    state = fields.Selection(
        related='stage_id.state',
        store=True,
    )
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('done', 'Ready for next stage'),
         ('blocked', 'Blocked')],
        'Kanban State',
        default='normal',
        track_visibility='onchange',
        help="A kanban state indicates special situations affecting it:\n"
        " * Normal is the default situation\n"
        " * Blocked indicates something is preventing"
        " the progress of this task\n"
        " * Ready for next stage indicates the"
        " task is ready to be pulled to the next stage",
        required=True, copy=False)

    # 2. Root Cause Analysis
    cause_ids = fields.Many2many(
        'mgmtsystem.nonconformity.cause',
        'mgmtsystem_nonconformity_cause_rel',
        'nonconformity_id',
        'cause_id',
        'Cause',
    )
    severity_id = fields.Many2one(
        'mgmtsystem.nonconformity.severity',
        'Severity',
    )
    analysis = fields.Text('Analysis')
    immediate_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Immediate action',
        domain="[('nonconformity_ids', '=', id)]",
    )

    # 3. Action Plan
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_nonconformity_action_rel',
        'nonconformity_id',
        'action_id',
        'Actions',
    )
    action_comments = fields.Text(
        'Action Plan Comments',
        help="Comments on the action plan.",
    )

    # 4. Effectiveness Evaluation
    evaluation_comments = fields.Text(
        'Evaluation Comments',
        help="Conclusions from the last effectiveness evaluation.",
    )

    # Multi-company
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id)

    corrective_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Corrective action',
        domain="[('nonconformity_id', '=', id)]",
    )
    preventive_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Preventive action',
        domain="[('nonconformity_id', '=', id)]",
    )

    @api.constrains('stage_id')
    def _check_close_with_evaluation(self):
        for nc in self:
            if nc.state == 'done' and not nc.evaluation_comments:
                raise models.ValidationError(
                    "Evaluation Comments are required "
                    "in order to close a Nonconformity.")

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('write_date')
    def _compute_days_since_updated(self, now_date=None):
        for nc in self:
            nc.days_since_updated = self._elapsed_days(
                self.create_date,
                self.write_date)

    @api.model
    def create(self, vals):
        vals.update({
            'ref': self.env['ir.sequence'].next_by_code(
                'mgmtsystem.nonconformity')
        })
        return super(MgmtsystemNonconformity, self).create(vals)

    @api.multi
    def write(self, vals):
        # Reset Kanban State on Stage change
        if 'stage_id' in vals:
            for nc in self:
                if nc.kanban_state != 'normal':
                    vals['kanban_state'] = 'normal'

        result = super(MgmtsystemNonconformity, self).write(vals)

        if False and 'is_writing' not in self.env.context:
            for nc in result.with_context(is_writing=True):
                if nc.state == 'done' and not nc.closing_date:
                    nc.closing_date = fields.Datetime.now()
                if nc.state != 'done' and nc.closing_date:
                    nc.closing_date = None
        return result
