# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Daniel Reis
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

from osv import fields, osv

class mgmtsystem_feedback_type(osv.osv):
    """Nonconformity/Feedback Type - Nonconformity, Good Practice, Improvement Opportunity, Observation, ..."""
    _name = "mgmtsystem.feedback.type"
    _description = "Feedback Type" 
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'description': fields.text('Description', translation=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }
mgmtsystem_feedback_type()


class mgmtsystem_feedback_categ(osv.osv):
    """Nonconformity/Feedback Category - specific area or topic regarded""" 
    _name = "mgmtsystem.feedback.categ"
    _description = "Feedback Category" 
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'description': fields.text('Description', translation=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }
mgmtsystem_feedback_categ()


class mgmtsystem_feedback_severity(osv.osv):
    """Nonconformity/Feedback Severity - Critical, Major, Minor, Invalid, ..."""
    _name = "mgmtsystem.feedback.severity"
    _description = "Severity of Complaints and Nonconformities"
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'sequence': fields.integer('Sequence',),
        'description': fields.text('Description', translation=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }
mgmtsystem_feedback_severity()


class mgmtsystem_nonconformity(osv.osv):
    _name = "mgmtsystem.nonconformity"
    _inherit = "mgmtsystem.nonconformity"
    _description = "Feedback and Nonconformities"
    _columns = {
        'categ_id': fields.many2one('mgmtsystem.feedback.categ', 'Category'),
        'audit_ids': fields.many2many('mgmtsystem.audit','mgmtsystem_audit_nonconformity_rel','mgmtsystem_audit_id','mgmtsystem_action_id','Related Audits'),
        'type_id': fields.many2one('mgmtsystem.feedback.type','Type'), 
        'severity_id': fields.many2one('mgmtsystem.feedback.severity', 'Severity'),
    }
mgmtsystem_nonconformity()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
