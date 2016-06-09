# -*- coding: utf-8 -*-

from openerp import fields, models,  _
from openerp import tools


class MgmtsystemtNonConformityReport(models.Model):
    """Management System Non Conformities Report."""

    _name = "mgmtsystem.nonconformity.report"
    _auto = False
    _description = "Management System Non Conformity Report"
    _rec_name = 'id'

    _STATES = [
        ('draft', _('Draft')),
        ('analysis', _('Analysis')),
        ('pending', _('Pending Approval')),
        ('open', _('In Progress')),
        ('done', _('Closed')),
        ('cancel', _('Cancelled')),
    ]

    # Compute data
    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True)
    age = fields.Integer('Age', readonly=True)
    number_of_days_to_analyse = fields.Integer(
        '# of days to analyse', readonly=True)
    number_of_days_to_plan = fields.Integer('# of days to plan', readonly=True)
    number_of_days_to_execute = fields.Integer(
        '# of days to execute', readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)

    # Grouping view

    date = fields.Datetime('Date', readonly=True, select=True)
    create_date = fields.Datetime('Create Date', readonly=True, select=True)
    analysis_date = fields.Datetime('Analysis Date', readonly=True,
                                    select=True)
    actions_date = fields.Datetime(
        'Action Plan evaluation Date', readonly=True, select=True)
    evaluation_date = fields.Datetime(
        'Efficiency evaluation Date', readonly=True, select=True)
    closing_date = fields.Datetime('Closing Date', readonly=True, select=True)
    cancel_date = fields.Datetime('Cancel Date', readonly=True, select=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    responsible_user_id = fields.Many2one(
        'res.users', 'Responsible', readonly=True)
    manager_user_id = fields.Many2one('res.users', 'Manager', readonly=True)
    author_user_id = fields.Many2one('res.users', 'Filled by', readonly=True)
    analysis_user_id = fields.Many2one('res.users', 'Analysis Evaluator',
                                       readonly=True)
    evaluation_user_id = fields.Many2one('res.users', 'Efficiency Evaluator',
                                         readonly=True)
    actions_user_id = fields.Many2one('res.users', 'Plan Evaluator',
                                      readonly=True)
    cause_ids = fields.Many2many(
        'mgmtsystem.nonconformity.cause',
        'mgmtsystem_nonconformity_cause_rel',
        'nonconformity_id',
        'cause_id',
        'Cause',
    )
    severity_id = fields.Many2one(
        'mgmtsystem.nonconformity.severity',
        'Severity', readonly=True,
    )
    origin_ids = fields.Many2many(
        'mgmtsystem.nonconformity.origin',
        'mgmtsystem_nonconformity_origin_rel',
        'nonconformity_id',
        'origin_id',
        'Origin'
    )
    procedure_ids = fields.Many2many(
        'document.page',
        'mgmtsystem_nonconformity_procedure_rel',
        'nonconformity_id',
        'procedure_id',
        'Procedure'
    )
    state = fields.Selection(_STATES, 'State')
    system_id = fields.Many2one('mgmtsystem.system', 'System', readonly=True)

    def init(self, cr):
        """Display a pivot view of non conformity."""
        tools.drop_view_if_exists(cr, 'mgmtsystem_nonconformity_report')
        cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_nonconformity_report AS (
                 select
                    m.id,
                    m.date as date,
                    m.create_date as create_date,
                    m.closing_date as closing_date,
                    m.cancel_date as cancel_date,
                    m.evaluation_date as evaluation_date,
                    m.actions_date as actions_date,
                    m.analysis_date as analysis_date,
                    m.manager_user_id,
                    m.author_user_id,
                    m.partner_id,
                    m.responsible_user_id,
                    m.analysis_user_id,
                    m.evaluation_user_id,
                    m.actions_user_id,
                    m.severity_id,
                    m.system_id,
                    m.state as state,


                    m.number_of_days_to_close as number_of_days_to_close,
                    m.number_of_days_to_plan as number_of_days_to_plan,
                    m.number_of_days_to_analyse as number_of_days_to_analyse,
                    m.number_of_days_to_execute as number_of_days_to_execute,
                    avg(extract('epoch' from (current_date-m.create_date))
                    )/(3600*24) as  age,
                    count(*) AS number_of_nonconformities
                from
                    mgmtsystem_nonconformity m
                group by m.partner_id, m.responsible_user_id, \
                        m.state, m.system_id, m.manager_user_id, \
                        m.author_user_id, m.analysis_user_id, \
                        m.actions_user_id, m.evaluation_user_id, \
                        m.create_date, m.analysis_date, m.actions_date, \
                        m.evaluation_date,  m.cancel_date, m.closing_date, \
                        m.date, m.id, m.number_of_days_to_close, \
                        m.number_of_days_to_plan,
                        m.number_of_days_to_analyse, \
                        m.number_of_days_to_execute
            )
            """)
