# -*- coding: utf-8 -*-

from openerp import fields, models
from openerp import tools


class MgmtsystemtAuditReport(models.Model):
    """Management System Action Report."""

    _name = "mgmtsystem.audit.report"
    _auto = False
    _description = "Management System Audit Report"
    _rec_name = 'id'

    # Compute data
    number_of_audits = fields.Integer('# of audits', readonly=True)
    age = fields.Integer('Age', readonly=True)
    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True)
    number_of_questions_in_verification_list = fields.Integer(
        '# of questions in verification list', readonly=True)
    number_of_improvements_opportunity = fields.Integer(
        '# of improvements Opportunities', readonly=True)
    number_of_exceeding_days = fields.Integer(
        '# of exceeding days', readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)

    # Grouping view
    create_date = fields.Datetime('Create Date', readonly=True, select=True)
    closing_date = fields.Datetime('Closing Date', readonly=True)
    user_id = fields.Many2one('res.users', 'Audit Manager', readonly=True)
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('done', 'Closed'),
        ],
        'State')
    system_id = fields.Many2one('mgmtsystem.system', 'System', readonly=True)

    def init(self, cr):
        """Display a pivot view of action."""
        tools.drop_view_if_exists(cr, 'mgmtsystem_audit_report')
        cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_audit_report AS (
                 select
                    m.id,
                    m.create_date as create_date,
                    m.closing_date as closing_date,
                    m.user_id,
                    m.system_id,
                    m.state as state,
                    avg(extract('epoch' from (current_date-m.create_date))
                    )/(3600*24) as  age,
                    m.number_of_days_to_close as number_of_days_to_close,
                    m.number_of_improvements_opportunity as
                    number_of_improvements_opportunity,
                    m.number_of_nonconformities as number_of_nonconformities,
                    m.number_of_questions_in_verification_list as
                     number_of_questions_in_verification_list,
                    count(*) AS number_of_audits
                from
                    mgmtsystem_audit m
                group by m.id, m.user_id, m.system_id, m.state, \
                        m.closing_date, m.create_date
            )
            """)
