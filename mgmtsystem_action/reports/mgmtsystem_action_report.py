
from odoo import fields, models, api
from odoo import tools


class MgmtsystemtActionReport(models.Model):
    """Management System Action Report."""

    _name = "mgmtsystem.action.report"
    _auto = False
    _description = "Management System Action Report"
    _rec_name = 'id'

    # Compute data
    number_of_actions = fields.Integer('# of actions', readonly=True)
    age = fields.Integer('Age', readonly=True)
    number_of_days_to_open = fields.Integer('# of days to open', readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)
    number_of_exceedings_days = fields.Integer(
        '# of exceedings days', readonly=True)

    # Grouping view
    type_action = fields.Selection([
        ('immediate', 'Immediate Action'),
        ('correction', 'Corrective Action'),
        ('prevention', 'Preventive Action'),
        ('improvement', 'Improvement Opportunity')
    ], 'Response Type')
    create_date = fields.Datetime('Create Date', readonly=True, index=True)
    date_open = fields.Datetime('Opening Date', readonly=True, index=True)
    date_closed = fields.Datetime('Close Date', readonly=True, index=True)
    date_deadline = fields.Date('Deadline', readonly=True, index=True)
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    stage_id = fields.Many2one(
        'mgmtsystem.action.stage', 'Stage', readonly=True)
    system_id = fields.Many2one('mgmtsystem.system', 'System', readonly=True)

    @api.model_cr
    def init(self):
        """Display a pivot view of action."""
        tools.drop_view_if_exists(self._cr, 'mgmtsystem_action_report')
        self.env.cr.execute("""
             CREATE OR REPLACE VIEW mgmtsystem_action_report AS (
                 select
                    m.id,
                    m.date_closed as date_closed,
                    m.date_deadline as date_deadline,
                    m.date_open as date_open,
                    m.user_id,
                    m.stage_id,
                    m.system_id,
                    m.type_action as type_action,
                    m.create_date as create_date,
                    m.number_of_days_to_open as number_of_days_to_open,
                    m.number_of_days_to_close as number_of_days_to_close,
                    avg(extract('epoch' from (current_date-m.create_date))
                    )/(3600*24) as  age,
                    avg(extract('epoch' from (m.date_closed - m.date_deadline))
                    )/(3600*24) as  number_of_exceedings_days,
                    count(*) AS number_of_actions
                from
                    mgmtsystem_action m
                group by m.user_id,m.system_id, m.stage_id, m.date_open, \
                        m.create_date,m.type_action,m.date_deadline, \
                        m.date_closed, m.id, m.number_of_days_to_open, \
                        m.number_of_days_to_close
            )
            """)
