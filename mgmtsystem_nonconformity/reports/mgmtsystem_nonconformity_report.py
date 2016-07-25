# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp import tools
from ..models.mgmtsystem_nonconformity_stage import _STATES


class MgmtsystemNonconformityReport(models.Model):
    """Management System NonConformity Report."""

    _name = "mgmtsystem.nonconformity.report"
    _auto = False
    _description = "Management System Non Conformity Report"
    _rec_name = 'id'

    # Compute data
    number_of_nonconformities = fields.Integer('# of nonconformities',
                                               readonly=True, default=1)
    age = fields.Integer('Age', readonly=True)
    number_of_days_to_analyse = fields.Integer(
        '# of days to analyse', readonly=True)
    number_of_days_to_plan = fields.Integer(
        '# of days to plan', readonly=True)
    number_of_days_to_execute = fields.Integer(
        '# of days to execute', readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)

    # Grouping view
    name = fields.Char('Name')
    create_date = fields.Datetime('Creation Date', readonly=True, select=True)
    closing_date = fields.Datetime('Closing Date', readonly=True, select=True)
    analysis_date = fields.Datetime(
        'Analysis Date',
        readonly=True, select=True
    )
    analysis_user_id = fields.Many2one(
        'res.users',
        'Analysis by',
        readonly=True,
    )

    evaluation_date = fields.Datetime(
        'Evaluation Date', readonly=True, select=True)
    evaluation_user_id = fields.Many2one(
        'res.users',
        'Evaluation by',
        readonly=True,
    )

    actions_date = fields.Datetime(
        'Action Plan Date', readonly=True, select=True)
    actions_user_id = fields.Many2one(
        'res.users',
        'Action Plan by',
        readonly=True,
    )

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)

    severity_id = fields.Many2one(
        'mgmtsystem.nonconformity.severity',
        'Severity',
    )

    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
        track_visibility="onchange"
    )
    manager_user_id = fields.Many2one(
        'res.users',
        'Manager',
        required=True,
        track_visibility="onchange"
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user.id,
        track_visibility="onchange"
    )

    state = fields.Selection(
        _STATES,
        'State'
    )
    system_id = fields.Many2one('mgmtsystem.system', 'System', readonly=True)

    def init(self, cr):
        """Display a pivot view of action."""
        tools.drop_view_if_exists(cr, 'mgmtsystem_nonconformity_report')
        cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_nonconformity_report AS (
                 select
                    m.id,
                    m.create_date as create_date,
                    m.closing_date as closing_date,
                    m.analysis_date as analysis_date,
                    m.evaluation_date as evaluation_date,
                    m.actions_date as actions_date,
                    m.partner_id,
                    m.actions_user_id,
                    m.evaluation_user_id,
                    m.analysis_user_id,
                    m.manager_user_id,
                    m.author_user_id,
                    m.responsible_user_id,
                    m.severity_id,
                    m.system_id,
                    m.name as name,
                    m.state as state,
                    m.number_of_days_to_close as number_of_days_to_close,
                    m.number_of_days_to_analyse as number_of_days_to_analyse,
                    m.number_of_days_to_execute as number_of_days_to_execute,
                    m.number_of_days_to_plan as number_of_days_to_plan,
                    avg(extract('epoch' from (current_date-m.create_date))
                    )/(3600*24) as  age,
                    count(*) AS number_of_nonconformities
                from
                    mgmtsystem_nonconformity m
                group by m.id,m.create_date, m.closing_date, m.analysis_date, \
                m.evaluation_date, m.actions_date, m.partner_id, \
                m.actions_user_id, m.evaluation_user_id, m.analysis_user_id, \
                m.manager_user_id, m.author_user_id, m.responsible_user_id, \
                m.severity_id, m.system_id, m.name, m.state
            )
            """)
