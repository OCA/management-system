# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tools.translate import _
from openerp import fields, models, api

from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)

from datetime import datetime
import time


def _own_company(self):
    """Return the user company id."""
    return self.env.user.company_id.id


class MgmtSystemAudit(models.Model):
    """Model class that manage audit."""
    _name = "mgmtsystem.audit"
    _description = "Audit"
    _inherit = ['mail.thread']
    name = fields.Char('Name', size=50)

    reference = fields.Char(
        'Reference',
        size=64,
        required=True,
        readonly=True,
        default='NEW'
    )
    date = fields.Datetime('Date')
    line_ids = fields.One2many(
        'mgmtsystem.verification.line',
        'audit_id',
        'Verification List',
    )
    quantity = fields.Integer('Number of audits', readonly=True, default=1)
    number_of_nonconformities = fields.Integer(
        'Number of nonconformities',
        compute='_number_of_nonconformity', readonly=True)
    number_of_questions_in_verification_list = fields.Integer(
        'Number of questions in verification list',
        compute='_number_of_questions_in_verification_list', readonly=True)
    number_of_improvements_opportunity = fields.Integer(
        'Number of improvements Opportunities',
        compute='_number_of_improvement_opportunity', readonly=True)

    closing_date = fields.Datetime('Closing Date', readonly=True)

    age = fields.Integer('Age', readonly=True, compute='_get_age')

    def _get_age(self):
        """Get audit current age."""
        return (
            datetime.now() - datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        ).days

    number_of_exceeding_days = fields.Integer(
        '# of exceeding days', readonly=True,
        compute='_get_number_of_exceeding_days')

    def _get_number_of_exceeding_days(self):
        """Get number of exceeding days."""
        return (
            datetime.now() - datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        ).days
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True)

    user_id = fields.Many2one('res.users', 'Audit Manager')
    auditor_user_ids = fields.Many2many(
        'res.users',
        'mgmtsystem_auditor_user_rel',
        'user_id',
        'mgmtsystem_audit_id',
        'Auditors',
    )
    auditee_user_ids = fields.Many2many(
        'res.users',
        'mgmtsystem_auditee_user_rel',
        'user_id',
        'mgmtsystem_audit_id',
        'Auditees',
    )
    strong_points = fields.Text('Strong Points')
    to_improve_points = fields.Text('Points To Improve')
    imp_opp_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_audit_imp_opp_rel',
        'mgmtsystem_action_id',
        'mgmtsystem_audit_id',
        'Improvement Opportunities',
    )

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity',
        string='Nonconformities',
    )
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('done', 'Closed'),
        ],
        'State',
        default="open"
    )
    system_id = fields.Many2one('mgmtsystem.system', 'System')
    company_id = fields.Many2one(
        'res.company', 'Company', default=_own_company)

    def _number_of_nonconformity(self):
        """Count number of nonconformities."""
        number = 0
        for id in self.nonconformity_ids:
            number = number + 1
        return number

    def _number_of_improvement_opportunity(self):
        """Count number of improvements Opportunities."""
        number = 0
        for id in self.imp_opp_ids:
            number = number + 1
        return number

    def _number_of_questions_in_verification_list(self):
        number = 0
        for id in self.line_ids:
            number = number + 1
        return number

    @api.model
    def create(self, vals):
        """Audit creation."""
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'mgmtsystem.audit'
            )
        })
        if vals.get('closing_date'):
            vals['closing_date'] = None
        return super(MgmtSystemAudit, self).create(vals)

    @api.model
    def button_close(self):
        """When Audit is closed, post a message to followers' chatter."""
        self.message_post(_("Audit closed"))
        number_of_days_to_close = (
            datetime.now() - datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        ).days
        return self.write({'state': 'done',
                           'closing_date': time.strftime(DATETIME_FORMAT),
                           'number_of_days_to_close': number_of_days_to_close})

    @api.multi
    def message_auto_subscribe1(self, updated_fields, values=None):
        """Automatically add the Auditors, Auditees and Audit Manager
        to the follow list
        """
        self.ensure_one()
        user_ids = [self.user_id.id]
        user_ids += [a.id for a in self.auditor_user_ids]
        user_ids += [a.id for a in self.auditee_user_ids]

        self.message_subscribe_users(user_ids=user_ids, subtype_ids=None)

        return super(MgmtSystemAudit, self).message_auto_subscribe(
            updated_fields=updated_fields,
            values=values
        )

    def get_action_url(self):
        """
        Return a short link to the audit form view
        eg. http://localhost:8069/?db=prod#id=1&model=mgmtsystem.audit
        """

        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url',
            default='http://localhost:8069'
        )
        url = ('{}/web#db={}&id={}&model={}').format(
            base_url,
            self.env.cr.dbname,
            self.id,
            self._name
        )
        return url


class MgmtSystemVerificationLine(models.Model):
    """Class to manage verification's Line."""
    _name = "mgmtsystem.verification.line"
    _description = "Verification Line"
    _order = "seq"

    name = fields.Char('Question', size=300, required=True)
    audit_id = fields.Many2one(
        'mgmtsystem.audit',
        'Audit',
        ondelete='cascade',
        select=True,
    )
    procedure_id = fields.Many2one(
        'document.page',
        'Procedure',
        ondelete='cascade',
        select=True,
    )
    is_conformed = fields.Boolean('Is conformed', default=False)
    comments = fields.Text('Comments')
    seq = fields.Integer('Sequence')
    company_id = fields.Many2one(
        'res.company', 'Company', default=_own_company)


class MgmtSystemNonconformity(models.Model):
    """Class use to add audit_ids association to MgmtSystemNonconformity."""
    _name = "mgmtsystem.nonconformity"
    _inherit = "mgmtsystem.nonconformity"
    audit_ids = fields.Many2many(
        'mgmtsystem.audit', string='Related Audits')
