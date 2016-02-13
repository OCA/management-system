# -*- coding: utf-8 -*-

from openerp import fields, models
from openerp import tools


class mgmtsystemt_action_report(models.Model):
    """ Management System Action Report"""

    _name = "mgmtsystem.action.report"
    _auto = False
    _description = "Management System Action Report"
    _rec_name = 'id'

    # Compute data
    number_of_actions = fields.Integer('# of actions', readonly=True)
    age = fields.Integer('Age', readonly=True)
    number_of_days_to_open = fields.Integer('# of days to open', readonly=True)
    number_of_days_to_close = fields.Integer('# of days to close', readonly=True)
    number_of_exceedings_days = fields.Integer('# of exceedings days', readonly=True)

    # Grouping view
    type_action = fields.Selection([
        ('immediate', 'Immediate Action'),
        ('correction', 'Corrective Action'),
        ('prevention', 'Preventive Action'),
        ('improvement', 'Improvement Opportunity')
        ], 'Response Type')
    action_date = fields.Datetime('Opening Date', readonly=True, select=True)
    create_date = fields.Datetime('Create Date', readonly=True, select=True)
    date_closed = fields.Datetime('Close Date', readonly=True, select=True)
    date_deadline = fields.Date('Deadline', readonly=True, select=True)
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    stage_id = fields.Many2one('mgmtsystem.action.stage', 'Stage', readonly=True)
    system_id = fields.Many2one('mgmtsystem.system', 'System', readonly=True)

    def init(self, cr):
        """
         Display a pivot view of action
        @param cr: the current row, from the database cursor,
         """
        tools.drop_view_if_exists(cr, 'mgmtsystem_action_report')
        cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_action_report AS (
                 select
                    m.id,
                    m.opening_date as opening_date,
                    m.date_closed as date_closed,
                    m.date_deadline as date_deadline,
                    m.user_id,
                    m.stage_id,
                    m.system_id,
                    m.type_action as type_action,
                    m.create_date as create_date,
                    avg(extract('epoch' from (current_date-m.create_date)))/(3600*24) as  age,
                    avg(extract('epoch' from (m.opening_date-m.create_date)))/(3600*24) as  number_of_days_to_open,
                    avg(extract('epoch' from (m.date_closed-m.create_date)))/(3600*24) as  number_of_days_to_close,
                    avg(extract('epoch' from (m.date_deadline - m.create_date)))/(3600*24) as  number_of_exceedings_days,
                    count(*) AS number_of_actions
                from
                    mgmtsystem_action m
                group by m.opening_date,\
                        m.user_id,m.system_id, m.stage_id, \
                        m.create_date,m.type_action,m.date_deadline,m.date_closed, m.id
            )
            """)
