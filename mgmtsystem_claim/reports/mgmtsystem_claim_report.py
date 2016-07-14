# -*- coding: utf-8 -*-

from openerp import fields, models
from openerp import tools


class MgmtsystemtClaimReport(models.Model):
    """Management System Claim Report."""

    _name = "mgmtsystem.claim.report"
    _auto = False
    _description = "Management System Claim Report"
    _rec_name = 'id'

    # Compute data
    number_of_claims = fields.Integer('# of claims', readonly=True)
    age = fields.Integer('Age', readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)
    number_of_exceedings_days = fields.Integer(
        '# of exceedings days', readonly=True)

    # Grouping view
    create_date = fields.Datetime('Create Date', readonly=True, select=True)
    write_date = fields.Datetime('Update Date', readonly=True, select=True)
    date_closed = fields.Datetime('Close Date', readonly=True, select=True)
    date_deadline = fields.Date('Deadline', readonly=True, select=True)
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    stage_id = fields.Many2one(
        'mgmtsystem.claim.stage', 'Stage', readonly=True)

    def init(self, cr):
        """Display a pivot view of claim."""
        tools.drop_view_if_exists(cr, 'mgmtsystem_claim_report')
        cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_claim_report AS (
                 select
                    m.id,
                    m.date_closed as date_closed,
                    m.date_deadline as date_deadline,
                    m.user_id,
                    m.stage_id,
                    m.create_date as create_date,
                    count(*) AS number_of_claims
                from
                    mgmtsystem_claim m
                group by m.user_id, m.stage_id, m.date, \
                        m.create_date,m.date_deadline, \
                        m.date_closed, m.id
            )
            """)
