# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from osv import fields, orm
from openerp.tools.translate import _


class EventScenarioLines(orm.Model):

    _name = "mgmtsystem.security.event.scenario"
    description = "Security Events - Scenario Lines"

    def __get_name(self, cr, uid, ids, field_name, arg, context):
        return self._get_name(cr, uid, ids, field_name, arg, context)

    _columns = {
        'name': fields.function(
            __get_name,
            type="char",
            method=True,
            string="Name"
        ),
        'description': fields.text('Description'),
        'scenario': fields.many2one(
            "mgmtsystem.security.threat.scenario", "Scenario"
        ),
        'origin': fields.many2one(
            "mgmtsystem.security.threat.origin", "Origin"
        ),
        'severity': fields.many2one(
            "mgmtsystem.severity", "Severity"
        ),
        'security_event_id': fields.many2one(
            "mgmtsystem.security.event", "Security Event"
        ),
    }

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        model = self.pool["mgmtsystem.security.event.scenario"]

        for obj in model.browse(cr, uid, ids):
            parts = [_("Events"), obj.scenario.name, obj.origin.name]
            res[obj.id] = " - ".join(parts)

        return res
