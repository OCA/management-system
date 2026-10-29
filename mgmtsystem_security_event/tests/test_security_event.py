# -*- coding: utf-8 -*-
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

from openerp.tests.common import TransactionCase


class TestCreateSecurityEventBase(TransactionCase):

    def get_severity(self, value, browse=False):
        res_id = self.severity_model.search(self.cr, self.uid, [
            ('value', '=', value),
            ('category', '=', 'security'),
        ])[0]
        if browse:
            return self.severity_model.browse(
                self.cr, self.uid, res_id, context=self.context)
        return res_id

    def get_probability(self, value, browse=False):
        res_id = self.probability_model.search(self.cr, self.uid, [
            ('value', '=', value),
            ('category', '=', 'security'),
        ])[0]
        if browse:
            return self.probability_model.browse(
                self.cr, self.uid, res_id, context=self.context)
        return res_id

    def setUp(self):
        super(TestCreateSecurityEventBase, self).setUp()

        self.system_model = self.registry('mgmtsystem.system')
        self.vector_model = self.registry(
            'mgmtsystem.security.vector')
        self.event_model = self.registry('mgmtsystem.security.event')
        self.probability_model = self.registry('mgmtsystem.probability')
        self.severity_model = self.registry('mgmtsystem.severity')
        self.user_model = self.registry('res.users')

        self.context = self.user_model.context_get(self.cr, self.uid)
        cr, uid, context = self.cr, self.uid, self.context

        self.system_id = self.system_model.create(cr, uid, {
            'name': 'Security System',
            'type': 'information_security',
        }, context=context)

        self.vector_id = self.vector_model.create(cr, uid, {
            'name': 'S1',
            'original_probability_id': self.get_probability(3),
            'original_severity_id': self.get_severity(4),
            'current_probability_id': self.get_probability(3),
            'current_severity_id': self.get_severity(3),
            'residual_probability_id': self.get_probability(1),
            'residual_severity_id': self.get_severity(2),
            'system_id': self.system_id,
        }, context=context)

        self.vector_2_id = self.vector_model.create(cr, uid, {
            'name': 'S2',
            'original_probability_id': self.get_probability(4),
            'original_severity_id': self.get_severity(4),
            'current_probability_id': self.get_probability(2),
            'current_severity_id': self.get_severity(2),
            'residual_probability_id': self.get_probability(2),
            'residual_severity_id': self.get_severity(1),
            'system_id': self.system_id,
        }, context=context)

        self.vector_3_id = self.vector_model.create(cr, uid, {
            'name': 'S3',
            'original_probability_id': self.get_probability(3),
            'original_severity_id': self.get_severity(3),
            'current_probability_id': self.get_probability(2),
            'current_severity_id': self.get_severity(1),
            'residual_probability_id': self.get_probability(2),
            'residual_severity_id': self.get_severity(1),
            'system_id': self.system_id,
        }, context=context)

        self.event_id = self.event_model.create(cr, uid, {
            'name': 'E1',
            'system_id': self.system_id,
            'scenario_ids': [
                (0, 0, {
                    'vector_id': self.vector_id,
                }),
                (0, 0, {
                    'vector_id': self.vector_2_id,
                }),
            ],
        }, context=context)

        self.event = self.event_model.browse(
            cr, uid, self.event_id, context=context)

        self.event_2_id = self.event_model.create(cr, uid, {
            'name': 'E2',
            'system_id': self.system_id,
            'scenario_ids': [
                (0, 0, {
                    'vector_id': self.vector_2_id,
                }),
                (0, 0, {
                    'vector_id': self.vector_3_id,
                }),
            ]
        }, context=context)

        self.event_2 = self.event_model.browse(
            cr, uid, self.event_2_id, context=context)


class TestCreateSecurityEvent(TestCreateSecurityEventBase):

    def test_event_multi_field(self):
        self.assertEqual(
            self.event.original_probability_id,
            self.get_probability(4, browse=True))

        self.assertEqual(
            self.event.original_severity_id,
            self.get_severity(4, browse=True))

        self.assertEqual(
            self.event.current_probability_id,
            self.get_probability(3, browse=True))

        self.assertEqual(
            self.event.current_severity_id,
            self.get_severity(3, browse=True))

        self.assertEqual(
            self.event.residual_probability_id,
            self.get_probability(2, browse=True))

        self.assertEqual(
            self.event.residual_severity_id,
            self.get_severity(2, browse=True))

    def test_event_multi_field_change_value(self):
        cr, uid, context = self.cr, self.uid, self.context

        self.vector_model.write(cr, uid, [self.vector_id], {
            'original_probability_id': self.get_probability(2),
            'original_severity_id': self.get_severity(2),
        }, context=context)

        self.vector_model.write(cr, uid, [self.vector_2_id], {
            'original_probability_id': self.get_probability(1),
            'original_severity_id': self.get_severity(1),
        }, context=context)

        self.event.refresh()

        self.assertEqual(
            self.event.original_probability_id,
            self.get_probability(2, browse=True))

        self.assertEqual(
            self.event.original_severity_id,
            self.get_severity(2, browse=True))
