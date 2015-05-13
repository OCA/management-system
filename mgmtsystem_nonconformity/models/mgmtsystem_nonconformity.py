# -*- coding: utf-8 -*-
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
<<<<<<< 06aa4f2b70a00af752d29b3a543ef5ebd33e203c

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
from tools.translate import _
import netsvc as netsvc
from openerp.osv import fields, orm
from openerp.addons.base_status.base_state import base_state

import time
from tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
=======
=======
>>>>>>> Added missing copyrights
from openerp.tools.translate import _
from openerp import netsvc
from openerp.exceptions import except_orm
from openerp import models, api, fields
=======

from openerp import models, api, fields, netsvc, exceptions, _
>>>>>>> Cleanup and full use of v8 and track features

from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)

import time
>>>>>>> Moved mgmtsystem_nonconformity to root for port


<<<<<<< 75bff4df4701f5ed835e70fe7acf4ab910086576:mgmtsystem_nonconformity/mgmtsystem_nonconformity.py
class mgmtsystem_nonconformity_cause(orm.Model):
    """
    Cause of the nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _order = 'parent_id, sequence'

    def name_get(self, cr, uid, ids, context=None):
        ids = ids or []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
    def _check_recursion(self, cr, uid, ids, context=None, parent=None):
        return super(mgmtsystem_nonconformity_cause, self)._check_recursion(cr, uid, ids, context=context, parent=parent)

=======
>>>>>>> Moved mgmtsystem_nonconformity to root for port
    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Cause', size=50, required=True, translate=True),
        'description': fields.text('Description'),
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        'sequence': fields.integer('Sequence', help="Defines the order to present items"),
        'parent_id': fields.many2one('mgmtsystem.nonconformity.cause', 'Group'),
        'child_ids': fields.one2many('mgmtsystem.nonconformity.cause', 'parent_id', 'Child Causes'),
        'ref_code': fields.char('Reference Code', size=20),
    }
    _constraints = [
        (_check_recursion, 'Error! Cannot create recursive cycle.', ['parent_id'])
=======
        'sequence': fields.integer(
            'Sequence',
            help="Defines the order to present items",
        ),
        'parent_id': fields.many2one(
            'mgmtsystem.nonconformity.cause',
            'Group',
        ),
        'child_ids': fields.one2many(
            'mgmtsystem.nonconformity.cause',
            'parent_id',
            'Child Causes',
        ),
        'ref_code': fields.char('Reference Code', size=20),
    }

    def _rec_message(self, cr, uid, ids, context=None):
        return _('Error! Cannot create recursive cycle.')

    _constraints = [
        (orm.BaseModel._check_recursion, _rec_message, ['parent_id'])
>>>>>>> Moved mgmtsystem_nonconformity to root for port
    ]


class mgmtsystem_nonconformity_origin(orm.Model):
    """
    Origin of nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.origin"
    _description = "Origin of nonconformity of the management system"
    _order = 'parent_id, sequence'

    def name_get(self, cr, uid, ids, context=None):
        ids = ids or []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
    def _check_recursion(self, cr, uid, ids, context=None, parent=None):
        return super(mgmtsystem_nonconformity_origin, self)._check_recursion(cr, uid, ids, context=context, parent=parent)

=======
>>>>>>> Moved mgmtsystem_nonconformity to root for port
    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Origin', size=50, required=True, translate=True),
        'description': fields.text('Description'),
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        'sequence': fields.integer('Sequence', help="Defines the order to present items"),
        'parent_id': fields.many2one('mgmtsystem.nonconformity.origin', 'Group'),
        'child_ids': fields.one2many('mgmtsystem.nonconformity.origin', 'parent_id', 'Childs'),
=======
        'sequence': fields.integer(
            'Sequence',
            help="Defines the order to present items",
        ),
        'parent_id': fields.many2one(
            'mgmtsystem.nonconformity.origin',
            'Group',
        ),
        'child_ids': fields.one2many(
            'mgmtsystem.nonconformity.origin',
            'parent_id',
            'Childs',
        ),
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        'ref_code': fields.char('Reference Code', size=20),
    }


<<<<<<< f843bb604319064d273a798a76021b9fa80fb3ab
=======
>>>>>>> Separated python in each model file:mgmtsystem_nonconformity/models/mgmtsystem_nonconformity.py
class mgmtsystem_nonconformity_severity(orm.Model):
    """Nonconformity Severity - Critical, Major, Minor, Invalid, ..."""
    _name = "mgmtsystem.nonconformity.severity"
    _description = "Severity of Complaints and Nonconformities"
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'sequence': fields.integer('Sequence',),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }


=======
>>>>>>> Removed severity redefined here
_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis')),
    ('pending', _('Pending Approval')),
    ('open', _('In Progress')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
]
_STATES_DICT = dict(_STATES)
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8

=======
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
=======
>>>>>>> Moved mgmtsystem_nonconformity to root for port


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _rec_name = "description"
    _inherit = ['mail.thread']
    _order = "date desc"
    _track = {
        'field': {
            'mgmtsystem_nonconformity.subtype_analysis': (
                lambda s, c, u, o, ctx=None: o["state"] == "analysis"
            ),
            'mgmtsystem_nonconformity.subtype_pending': (
                lambda s, c, u, o, ctx=None: o["state"] == "pending"
            ),
        },
    }

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

<<<<<<< 94f11df8d4c77ee3a7feebf4d1370e1528414857
<<<<<<< 4590be07d52726216d516d3763733db0e6d138c7
    _columns = {
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        #1. Description
=======
        # 1. Description
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        'id': fields.integer('ID', readonly=True),
        'ref': fields.char('Reference', size=64, required=True, readonly=True),
        'date': fields.date('Date', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'reference': fields.char('Related to', size=50),
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        'responsible_user_id': fields.many2one('res.users', 'Responsible', required=True),
        'manager_user_id': fields.many2one('res.users', 'Manager', required=True),
        'author_user_id': fields.many2one('res.users', 'Filled in by', required=True),
        'origin_ids': fields.many2many('mgmtsystem.nonconformity.origin', 'mgmtsystem_nonconformity_origin_rel', 'nonconformity_id', 'origin_id', 'Origin', required=True),
        'procedure_ids': fields.many2many('document.page', 'mgmtsystem_nonconformity_procedure_rel', 'nonconformity_id', 'procedure_id', 'Procedure'),
        'description': fields.text('Description', required=True),
        'state': fields.selection(_STATES, 'State', readonly=True),
        'state_name': fields.function(_state_name, string='State Description', type='char', size=40),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
<<<<<<< df913a09410052efe02604e09f25e52d3005cf5f
=======
        'message_ids': fields.one2many('mail.message', 'res_id', 'Messages', domain=[('model', '=', _name)]),
>>>>>>> [FIX] PEP8 compliance after running flake8
        #2. Root Cause Analysis
        'cause_ids': fields.many2many('mgmtsystem.nonconformity.cause', 'mgmtsystem_nonconformity_cause_rel', 'nonconformity_id', 'cause_id', 'Cause'),
        'severity_id': fields.many2one('mgmtsystem.nonconformity.severity', 'Severity'),
        'analysis': fields.text('Analysis'),
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8
        'immediate_action_id': fields.many2one('mgmtsystem.action', 'Immediate action', domain="[('nonconformity_id', '=', id)]"),
=======
        'immediate_action_id': fields.many2one('mgmtsystem.action', 'Immediate action', domain="[('nonconformity_id','=',id)]"),
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
        'analysis_date': fields.datetime('Analysis Date', readonly=True),
        'analysis_user_id': fields.many2one('res.users', 'Analysis by', readonly=True),
        #3. Action Plan
        'action_ids': fields.many2many('mgmtsystem.action', 'mgmtsystem_nonconformity_action_rel', 'nonconformity_id', 'action_id', 'Actions'),
        'actions_date': fields.datetime('Action Plan Date', readonly=True),
        'actions_user_id': fields.many2one('res.users', 'Action Plan by', readonly=True),
        'action_comments': fields.text('Action Plan Comments', help="Comments on the action plan."),
        #4. Effectiveness Evaluation
        'evaluation_date': fields.datetime('Evaluation Date', readonly=True),
        'evaluation_user_id': fields.many2one('res.users', 'Evaluation by', readonly=True),
        'evaluation_comments': fields.text('Evaluation Comments', help="Conclusions from the last effectiveness evaluation."),
=======
        'responsible_user_id': fields.many2one(
            'res.users',
            'Responsible',
            required=True,
        ),
        'manager_user_id': fields.many2one(
            'res.users',
            'Manager',
            required=True,
        ),
        'author_user_id': fields.many2one(
            'res.users',
            'Filled in by',
            required=True,
        ),
        'origin_ids': fields.many2many(
            'mgmtsystem.nonconformity.origin',
            'mgmtsystem_nonconformity_origin_rel',
            'nonconformity_id',
            'origin_id', 'Origin', required=True,
        ),
        'procedure_ids': fields.many2many(
            'document.page', 'mgmtsystem_nonconformity_procedure_rel',
            'nonconformity_id', 'procedure_id', 'Procedure'
        ),
        'description': fields.text('Description', required=True),
        'state': fields.selection(_STATES, 'State', readonly=True),
        'state_name': fields.function(
            _state_name,
            string='State Description',
            type='char',
            size=40,
        ),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        # 2. Root Cause Analysis
        'cause_ids': fields.many2many(
            'mgmtsystem.nonconformity.cause',
            'mgmtsystem_nonconformity_cause_rel',
            'nonconformity_id',
            'cause_id',
            'Cause',
        ),
        'severity_id': fields.many2one(
            'mgmtsystem.nonconformity.severity',
            'Severity',
        ),
        'analysis': fields.text('Analysis'),
        'immediate_action_id': fields.many2one(
            'mgmtsystem.action',
            'Immediate action',
            domain="[('nonconformity_id', '=', id)]",
        ),
        'analysis_date': fields.datetime('Analysis Date', readonly=True),
        'analysis_user_id': fields.many2one(
            'res.users',
            'Analysis by',
            readonly=True,
        ),
        # 3. Action Plan
        'action_ids': fields.many2many(
            'mgmtsystem.action',
            'mgmtsystem_nonconformity_action_rel',
            'nonconformity_id',
            'action_id',
            'Actions',
        ),
        'actions_date': fields.datetime('Action Plan Date', readonly=True),
        'actions_user_id': fields.many2one(
            'res.users',
            'Action Plan by',
            readonly=True,
        ),
        'action_comments': fields.text(
            'Action Plan Comments',
            help="Comments on the action plan.",
        ),
        # 4. Effectiveness Evaluation
        'evaluation_date': fields.datetime('Evaluation Date', readonly=True),
        'evaluation_user_id': fields.many2one(
            'res.users',
            'Evaluation by',
            readonly=True,
        ),
        'evaluation_comments': fields.text(
            'Evaluation Comments',
            help="Conclusions from the last effectiveness evaluation.",
        ),
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        # Multi-company
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
=======
        'company_id': (
            lambda self, cr, uid, c:
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id),
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        'date': lambda *a: time.strftime(DATE_FORMAT),
        'state': 'draft',
        'author_user_id': lambda cr, uid, id, c={}: id,
        'ref': 'NEW',
    }
=======
=======
    name = fields.Char('Name')

>>>>>>> Added missing fields (used in demo data)
    # 1. Description
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )
    date = fields.Date(
        'Date',
        required=True,
        default=lambda *a: time.strftime(DATE_FORMAT)
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    reference = fields.Char('Related to')
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
    )
    manager_user_id = fields.Many2one(
        'res.users',
        'Manager',
        required=True,
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user.id
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
    state = fields.Selection(
        _STATES,
        'State',
        readonly=True,
        default="draft",
        track_visibility='onchange',
    )
    state_name = fields.Char(
        compute='_state_name',
        string='State Description',
    )
    system_id = fields.Many2one('mgmtsystem.system', 'System')

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
        domain="[('nonconformity_id', '=', id)]",
    )
    analysis_date = fields.Datetime(
        'Analysis Date',
        readonly=True,
        track_visibility='onchange',
    )
    analysis_user_id = fields.Many2one(
        'res.users',
        'Analysis by',
        readonly=True,
        track_visibility='onchange',
    )

    # 3. Action Plan
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_nonconformity_action_rel',
        'nonconformity_id',
        'action_id',
        'Actions',
    )
    actions_date = fields.Datetime('Action Plan Date', readonly=True)
    actions_user_id = fields.Many2one(
        'res.users',
        'Action Plan by',
        readonly=True,
    )
    action_comments = fields.Text(
        'Action Plan Comments',
        help="Comments on the action plan.",
    )

    # 4. Effectiveness Evaluation
    evaluation_date = fields.Datetime('Evaluation Date', readonly=True)
    evaluation_user_id = fields.Many2one(
        'res.users',
        'Evaluation by',
        readonly=True,
    )
    evaluation_comments = fields.Text(
        'Evaluation Comments',
        help="Conclusions from the last effectiveness evaluation.",
    )

    # Multi-company
<<<<<<< be1ad52fa3ab11b8bd762f60fde4735b13bd6441
    company_id = fields.Many2one('res.company', 'Company', default=own_company)
>>>>>>> Ported fields to v8
=======
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id)
>>>>>>> Removed ID and removed named lambdas

    # Demo data missing fields...
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

    @property
    @api.multi
    def verbose_name(self):
        return self.env['ir.model'].search([('model', '=', self._name)]).name

    @api.model
    def create(self, vals):
        vals.update({
<<<<<<< 0781fe6305aed8cc6e869575b3e1d285d6219f55
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
            'ref': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.nonconformity')
        })
        return super(mgmtsystem_nonconformity, self).create(cr, uid, vals, context)

    def message_auto_subscribe(self, cr, uid, ids, updated_fields, context=None, values=None):
        """Add the reponsible, manager and OpenChatter follow list."""
        o = self.browse(cr, uid, ids, context=context)[0]
        user_ids = [o.responsible_user_id.id, o.manager_user_id.id, o.author_user_id.id]
        self.message_subscribe_users(cr, uid, ids, user_ids=user_ids, subtype_ids=None, context=context)
        return super(mgmtsystem_nonconformity, self).message_auto_subscribe(cr, uid, ids, updated_fields=updated_fields, context=context, values=values)
=======
            'ref': self.pool.get('ir.sequence').get(
                cr, uid, 'mgmtsystem.nonconformity')
=======
            'ref': self.env['ir.sequence'].get('mgmtsystem.nonconformity')
>>>>>>> Added tests for create nonconformity
        })
        return super(MgmtsystemNonconformity, self).create(vals)

    @api.multi
    def message_auto_subscribe(self, updated_fields, values=None):
        """Add the responsible, manager and OpenChatter follow list."""
        self.ensure_one()
        user_ids = [
            self.responsible_user_id.id,
            self.manager_user_id.id,
            self.author_user_id.id,
        ]
        self.message_subscribe_users(user_ids=user_ids, subtype_ids=None)
        return super(MgmtsystemNonconformity, self).message_auto_subscribe(
            updated_fields=updated_fields,
            values=values
        )
>>>>>>> Moved mgmtsystem_nonconformity to root for port

<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
<<<<<<< 2024a34797b9dc184b846f5ee3e9771d37c76175
    def case_send_note(self, cr, uid, ids, text, data=None, context=None):
        for id in ids:
            pre = self.case_get_note_msg_prefix(cr, uid, id, context=context)
            msg = '%s <b>%s</b>' % (pre, text)
            if data:
                o = self.browse(cr, uid, ids, context=context)[0]
<<<<<<< 71aa0a8a6f4f4f006d1786851185cfac782618dd
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
                post = _('\n<br />\n<ul><li> <b>Stage:</b> %s \xe2\x86\x92 %s</li></ul>') % (o.state, data['state'])
=======
                post = _('''
=======
                post = _(u'''
>>>>>>> Updated module as installable and removed depdencie on base_status
<br />
<ul><li> <b>State:</b> %s → %s</li></ul>\
''') % (o.state, data['state'])
>>>>>>> Moved mgmtsystem_nonconformity to root for port
                msg += post
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_get_note_msg_prefix(self, cr, uid, id, context=None):
        return _('Nonconformity')

=======
>>>>>>> Use track and mail message subtypes instead of overriding functions
    def wkf_analysis(self, cr, uid, ids, context=None):
=======
    @api.multi
    def wkf_analysis(self):
>>>>>>> Cleanup and full use of v8 and track features
        """Change state from draft to analysis"""
        return self.write({
            'state': 'analysis',
            'analysis_date': None,
            'analysis_user_id': None}
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
<<<<<<< 2024a34797b9dc184b846f5ee3e9771d37c76175
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        self.case_send_note(cr, uid, ids, _('Analysis'), data=data, context=context)
=======
        self.case_send_note(
            cr, uid, ids, _('Analysis'), data=data, context=context
        )
>>>>>>> Moved mgmtsystem_nonconformity to root for port
=======
>>>>>>> Use track and mail message subtypes instead of overriding functions
        return self.write(cr, uid, ids, data, context=context)
=======
        )
>>>>>>> Cleanup and full use of v8 and track features

    @api.multi
    def action_sign_analysis(self):
        """Sign-off the analysis"""
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'analysis':
<<<<<<< c78ad3ce9f0ea5ee98baa923b2662899cec0c8cc
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
            raise orm.except_orm(_('Error !'), _('This action can only be done in the Analysis state.'))
        if o.analysis_date:
            raise orm.except_orm(_('Error !'), _('Analysis is already approved.'))
        if not o.analysis:
            raise orm.except_orm(_('Error !'), _('Please provide an analysis before approving.'))
        vals = {'analysis_date': time.strftime(DATETIME_FORMAT), 'analysis_user_id': uid}
=======
            raise orm.except_orm(
=======
            raise except_orm(
>>>>>>> Get exceptions without importing orm
                _('Error !'),
=======
        self.ensure_one()
        if self.state != 'analysis':
            raise exceptions.ValidationError(
>>>>>>> Cleanup and full use of v8 and track features
                _('This action can only be done in the Analysis state.')
            )
        if self.analysis_date:
            raise exceptions.ValidationError(
                _('Analysis is already approved.')
            )
        if not self.analysis:
            raise exceptions.ValidationError(
                _('Please provide an analysis before approving.')
            )
        self.write({
            'analysis_date': time.strftime(DATETIME_FORMAT),
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
            'analysis_user_id': uid,
        }
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        self.write(cr, uid, ids, vals, context=context)
        msg = '%s <b>%s</b>' % (self._description, _('Analysis Approved'))
        self.message_post(cr, uid, ids, body=msg, context=context)
=======
            'analysis_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (self.verbose_name, _('Analysis Approved'))
        )
>>>>>>> Cleanup and full use of v8 and track features
        return True

    @api.multi
    def wkf_review(self):
        """Change state from analysis to pending approval"""
        for o in self:
            if not o.analysis_date:
                raise exceptions.ValidationError(
                    _('Analysis must be performed before submitting to '
                      'approval.')
                )
        return self.write({
            'state': 'pending',
            'actions_date': None,
            'actions_user_id': None}
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
<<<<<<< 2024a34797b9dc184b846f5ee3e9771d37c76175
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        self.case_send_note(cr, uid, ids, _('Pending Approval'), data=vals, context=context)
=======
        self.case_send_note(
            cr, uid, ids, _('Pending Approval'), data=vals, context=context
        )
>>>>>>> Moved mgmtsystem_nonconformity to root for port
=======
>>>>>>> Use track and mail message subtypes instead of overriding functions
        return self.write(cr, uid, ids, vals, context=context)
=======
        )
>>>>>>> Cleanup and full use of v8 and track features

    @api.multi
    def action_sign_actions(self):
        """Sign-off the action plan"""
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'pending':
<<<<<<< c78ad3ce9f0ea5ee98baa923b2662899cec0c8cc
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
            raise orm.except_orm(_('Error !'), _('This action can only be done in the Pending for Approval state.'))
        if o.actions_date:
            raise orm.except_orm(_('Error !'), _('Action plan is already approved.'))
        if not self.browse(cr, uid, ids, context=context)[0].analysis_date:
            raise orm.except_orm(_('Error !'), _('Analysis approved before the review confirmation.'))
        vals = {'actions_date': time.strftime(DATETIME_FORMAT), 'actions_user_id': uid}
=======
            raise orm.except_orm(
=======
            raise except_orm(
>>>>>>> Get exceptions without importing orm
                _('Error !'),
=======
        self.ensure_one()
        if self.state != 'pending':
            raise exceptions.ValidationError(
>>>>>>> Cleanup and full use of v8 and track features
                _('This action can only be done in the Pending for Approval '
                  'state.')
            )
        if self.actions_date:
            raise exceptions.ValidationError(
                _('Action plan is already approved.')
            )
        if not self.analysis_date:
            raise exceptions.ValidationError(
                _('Analysis approved before the review confirmation.')
            )
        self.write({
            'actions_date': time.strftime(DATETIME_FORMAT),
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
            'actions_user_id': uid,
        }
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        self.write(cr, uid, ids, vals, context=context)
        msg = '%s <b>%s</b>' % (self._description, _('Action Plan Approved'))
        self.message_post(cr, uid, ids, body=msg, context=context)
        return True

    def wkf_open(self, cr, uid, ids, context=None):
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        """Change state from pending approval to in progress, and Open  the related actions"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.actions_date:
            raise orm.except_orm(_('Error !'), _('Action plan must be approved before opening.'))
        self.case_open_send_note(cr, uid, ids, context=context)
        #Open related Actions
=======
=======
            'actions_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (
                self.verbose_name, _('Action Plan Approved')
            )
        )
        return True

    @api.multi
    def wkf_open(self):
>>>>>>> Cleanup and full use of v8 and track features
        """Change state from pending approval to in progress, and Open
        the related actions
        """
        self.ensure_one()
        if not self.actions_date:
            raise exceptions.ValidationError(
                _('Action plan must be approved before opening.')
            )
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        self.case_open_send_note(cr, uid, ids, context=context)
<<<<<<< 708ae9983cca04e4dee06cfde6c7c3070f93e28b
        # Open related Actions
<<<<<<< 6794e3612a1105b8d45a05fbe2bd17eca30cd25f
<<<<<<< b7b2c1a83a414b319605200700d3b02067ba784d
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        if o.immediate_action_id and o.immediate_action_id.state == 'draft':
=======
        # TODO static variables... hmm
=======
        # TODO static variables... hmm update state isn't going to work
<<<<<<< 75bff4df4701f5ed835e70fe7acf4ab910086576:mgmtsystem_nonconformity/mgmtsystem_nonconformity.py
>>>>>>> Use stage_id for actions
        if o.immediate_action_id and o.immediate_action_id.stage_id.name.lower() == 'draft':
>>>>>>> Small fix to use stage_id.name instead of state
=======
        if (o.immediate_action_id
                and o.immediate_action_id.stage_id.name.lower() == 'draft'):
>>>>>>> Separated python in each model file:mgmtsystem_nonconformity/models/mgmtsystem_nonconformity.py
=======

<<<<<<< 13e1999046b4defdeb03ea2574d58c112dd67470
        if o.immediate_action_id and o.immediate_action_id.stage_id.is_starting:
>>>>>>> Use stage is ending and is starting instead of by name
=======
        if (o.immediate_action_id and
                o.immediate_action_id.stage_id.is_starting):
>>>>>>> Fix flake8 errors
            o.immediate_action_id.case_open()
        for a in o.action_ids:
            if a.stage_id.is_starting:
                a.case_open()
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        return self.write(cr, uid, ids, {'state': 'open', 'evaluation_date': None, 'evaluation_user_id': None}, context=context)
=======
        return self.write(cr, uid, ids, {
            'state': 'open',
            'evaluation_date': None,
            'evaluation_user_id': None,
        }, context=context)
>>>>>>> Moved mgmtsystem_nonconformity to root for port
=======
        if (self.immediate_action_id and
                self.immediate_action_id.stage_id.is_starting):
            self.immediate_action_id.case_open()
        for action in self.action_ids:
            if action.stage_id.is_starting:
                action.case_open()
        return self.write({
            'state': 'open',
            'evaluation_date': False,
            'evaluation_user_id': False,
        })
>>>>>>> Cleanup and full use of v8 and track features

    @api.one
    def action_sign_evaluation(self):
        """Sign-off the effectiveness evaluation"""
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'open':
<<<<<<< c78ad3ce9f0ea5ee98baa923b2662899cec0c8cc
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
            raise orm.except_orm(_('Error !'), _('This action can only be done in the In Progress state.'))
        vals = {'evaluation_date': time.strftime(DATETIME_FORMAT), 'evaluation_user_id': uid}
=======
            raise orm.except_orm(
=======
            raise except_orm(
>>>>>>> Get exceptions without importing orm
                _('Error !'),
=======
        if self.state != 'open':
            raise exceptions.ValidationError(
>>>>>>> Cleanup and full use of v8 and track features
                _('This action can only be done in the In Progress state.')
            )
        self.write({
            'evaluation_date': time.strftime(DATETIME_FORMAT),
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
            'evaluation_user_id': uid,
        }
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        self.write(cr, uid, ids, vals, context=context)
        msg = '%s <b>%s</b>' % (
            self._description, _('Effectiveness Evaluation Approved')
=======
            'evaluation_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (
                self.verbose_name, _('Effectiveness Evaluation Approved')
            )
>>>>>>> Cleanup and full use of v8 and track features
        )

    @api.multi
    def wkf_cancel(self):
        """Change state to cancel"""
        return self.write({'state': 'cancel'})

    @api.multi
    def wkf_close(self):
        """Change state from in progress to closed"""
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        o = self.browse(cr, uid, ids, context=context)[0]
<<<<<<< 13e1999046b4defdeb03ea2574d58c112dd67470
<<<<<<< 5836488589af7e4b33185380a39618e98d33991e
<<<<<<< 2ec8386018ef68321e61e374bab7e40164f20988
        done_states = ['done', 'cancelled']
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        if (o.immediate_action_id and o.immediate_action_id.state not in done_states):
            raise orm.except_orm(_('Error !'), _('Immediate action from analysis has not been closed.'))
        if ([i for i in o.action_ids if i.state not in done_states]):
            raise orm.except_orm(_('Error !'), _('Not all actions have been closed.'))
        if not o.evaluation_date:
            raise orm.except_orm(_('Error !'), _('Effectiveness evaluation must be performed before closing.'))
=======
=======
        # TODO make it more friendly
        done_states = ['done', 'cancelled', 'settled', 'rejected']
>>>>>>> Add support for settled, rejected instead of done/canceled... quite ugly
=======
        done_stages = ['settled', 'rejected']
=======
>>>>>>> Fix flake8 errors

>>>>>>> Remove states as we are using stages on actions...
        if (o.immediate_action_id
                and not o.immediate_action_id.stage_id.is_ending):
            raise except_orm(
                _('Error !'),
=======
        self.ensure_one()

        if (self.immediate_action_id
                and not self.immediate_action_id.stage_id.is_ending):
            raise exceptions.ValidationError(
>>>>>>> Cleanup and full use of v8 and track features
                _('Immediate action from analysis has not been closed.')
            )
        if any(i for i in self.action_ids if not i.stage_id.is_ending):
            raise exceptions.ValidationError(
                _('Not all actions have been closed.')
            )
        if not self.evaluation_date:
            raise exceptions.ValidationError(
                _('Effectiveness evaluation must be performed before closing.')
            )
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        self.case_close_send_note(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)
=======
        return self.write({'state': 'done'})
>>>>>>> Cleanup and full use of v8 and track features

    @api.multi
    def case_reset(self):
        """Reset to Draft and restart the workflow"""
        wf_service = netsvc.LocalService("workflow")
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        for id in ids:
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8
<<<<<<< df913a09410052efe02604e09f25e52d3005cf5f
            res = wf_service.trg_create(uid, self._name, id, cr)
=======
            wf_service.trg_create(uid, self._name, id, cr)
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
        self.case_reset_send_note(cr, uid, ids, context=context)
=======
            wf_service.trg_create(uid, self._name, id, cr)
        self.message_post(cr, uid, self.browse(cr, uid, ids, context=context), _('Draft'))
>>>>>>> [FIX] PEP8 compliance after running flake8
=======
            wf_service.trg_create(uid, self._name, id, cr)
        self.case_reset_send_note(cr, uid, ids, context=context)
>>>>>>> Moved mgmtsystem_nonconformity to root for port
        vals = {
=======
        for nc in self:
            wf_service.trg_create(self._uid, self._name, nc.id, self._cr)
        return self.write({
>>>>>>> Cleanup and full use of v8 and track features
            'state': 'draft',
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
<<<<<<< c2538af8ebe5dc74b251cb209e1c58e9c4d99446
        }
        return self.write(cr, uid, ids, vals, context=context)
<<<<<<< 2394dcc563549fe896d383a41c8d1e4640172f11

    def case_cancel_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>canceled</b>.') % self._description
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_reset_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>renewed</b>.') % self._description
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_open_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>opened</b>.') % self._description
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True
<<<<<<< bbf6fed93779d713aeaa0215af3019389b5a738b
<<<<<<< 75bff4df4701f5ed835e70fe7acf4ab910086576:mgmtsystem_nonconformity/mgmtsystem_nonconformity.py


class mgmtsystem_action(orm.Model):
    _inherit = "mgmtsystem.action"
    _columns = {
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
        'nonconformity_immediate_id': fields.one2many('mgmtsystem.nonconformity', 'immediate_action_id', readonly=True),
        'nonconformity_ids': fields.many2many('mgmtsystem.nonconformity', 'mgmtsystem_nonconformity_action_rel', 'action_id', 'nonconformity_id', 'Nonconformities', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
        'nonconformity_immediate_id': fields.one2many(
            'mgmtsystem.nonconformity',
            'immediate_action_id',
            readonly=True,
        ),
        'nonconformity_ids': fields.many2many(
            'mgmtsystem.nonconformity',
            'mgmtsystem_nonconformity_action_rel',
            'action_id',
            'nonconformity_id',
            'Nonconformities',
            readonly=True,
        ),
    }
>>>>>>> Moved mgmtsystem_nonconformity to root for port
=======
>>>>>>> Separated python in each model file:mgmtsystem_nonconformity/models/mgmtsystem_nonconformity.py
=======

    def case_close_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>closed</b>.') % self._description
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True
>>>>>>> Added missing methodcase_close_send_note for workflows
=======
>>>>>>> Remove unused functions
=======
        })
>>>>>>> Cleanup and full use of v8 and track features
