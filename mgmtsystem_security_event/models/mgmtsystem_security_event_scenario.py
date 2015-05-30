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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class EventScenarioLines(orm.Model):

    """
    Event Scenario Lines.

    The event scenario lines are used inside the
    security event model.
    """

    _name = "mgmtsystem.security.event.scenario"
    _description = "Security Events - Scenario Lines"

    _columns = {
        'description': fields.text('Description'),
        'scenario_id': fields.many2one(
            "mgmtsystem.security.threat.scenario", "Scenario"
        ),
        'origin_id': fields.many2one(
            "mgmtsystem.security.threat.origin", "Origin"
        ),
        'probability_id': fields.many2one(
            "mgmtsystem.probability", "Probability"
        ),
        'security_event_id': fields.many2one(
            "mgmtsystem.security.event", "Security Event"
        ),
        'system_id': fields.related(
            'security_event_id',
            'system_id',
            string='System',
            readonly=True,
            type='many2one',
            relation='mgmtsystem.system',
            store=True,
        ),
    }

    def name_get(self, cr, uid, ids, context=None):
        """
        The method gets the name of the objects referenced by ids.

        This method computes the name based on the measures and
        underlying_assets fields. It computes the name for each ids
        and can be extended by subclass.
        """
        res = {}

        for obj in self.browse(cr, uid, ids, context=context):
            parts = [_("Events"),
                     obj.scenario.name,
                     obj.origin.name]
            res[obj.id] = " - ".join(parts)

        return res
