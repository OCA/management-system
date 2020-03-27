# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields, _


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "create_date desc"

    @api.model
    def _default_stage(self):
        """Return the default stage."""
        return (
            self.env.ref('mgmtsystem_nonconformity.stage_draft', False) or
            self.env['mgmtsystem.nonconformity.stage'].search(
                [('is_starting', '=', True)],
                limit=1))

    @api.model
    def _stage_groups(self, stages, domain, order):
        stage_ids = self.env['mgmtsystem.nonconformity.stage'].search([])
        return stage_ids

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
    user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user,
        track_visibility=True,
        oldname="author_user_id",  # automatic migration
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
        default=_default_stage, group_expand='_stage_groups')
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
        required=True,
        copy=False,
    )

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

    @api.multi
    def _get_all_actions(self):
        self.ensure_one()
        return (
            self.action_ids +
            self.immediate_action_id)

    @api.constrains('stage_id')
    def _check_open_with_action_comments(self):
        for nc in self:
            if nc.state == 'open' and not nc.action_comments:
                raise models.ValidationError(
                    _("Action plan  comments are required "
                      "in order to put a nonconformity In Progress."))

    @api.constrains('stage_id')
    def _check_close_with_evaluation(self):
        for nc in self:
            if nc.state == 'done':
                if not nc.evaluation_comments:
                    raise models.ValidationError(
                        _("Evaluation Comments are required "
                          "in order to close a Nonconformity."))
                actions_are_closed = (
                    x.stage_id.is_ending
                    for x in nc._get_all_actions())
                if not all(actions_are_closed):
                    raise models.ValidationError(
                        _("All actions must be done "
                          "before closing a Nonconformity."))

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('closing_date', 'create_date')
    def _compute_number_of_days_to_close(self):
        for nc in self:
            nc.number_of_days_to_close_open = self._elapsed_days(
                nc.create_date,
                nc.closing_date)

    @api.depends('write_date')
    def _compute_days_since_updated(self):
        for nc in self:
            nc.days_since_updated = self._elapsed_days(
                nc.create_date,
                nc.write_date)

    @api.model
    def create(self, vals):
        vals.update({
            'ref': self.env['ir.sequence'].next_by_code(
                'mgmtsystem.nonconformity')
        })
        return super().create(vals)

    @api.multi
    def write(self, vals):
        is_writing = 'is_writing' in self.env.context
        is_state_change = 'stage_id' in vals or 'state' in vals
        # Reset Kanban State on Stage change
        if is_state_change:
            was_not_open = {
                x.id: x.state in ('draft',
                                  'analysis', 'pending') for x in self}
            for nc in self:
                if nc.kanban_state != 'normal':
                    vals['kanban_state'] = 'normal'

        result = super().write(vals)

        # Set/reset the closing date
        if not is_writing and is_state_change:
            for nc in self.with_context(is_writing=True):
                # On Close set Closing Date
                if nc.state == 'done' and not nc.closing_date:
                    nc.closing_date = fields.Datetime.now()
                # On reopen resete Closing Date
                if nc.state != 'done' and nc.closing_date:
                    nc.closing_date = None
                # On action plan approval, Open the Actions
                if nc.state == 'open' and was_not_open[nc.id]:
                    for action in nc._get_all_actions():
                        if action.stage_id.is_starting:
                            action.case_open()
        return result
