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

from openerp.addons.mgmtsystem_security_event.tests.test_security_event \
    import TestCreateSecurityEventBase

from openerp.netsvc import LocalService


class TestRiskMatrix(TestCreateSecurityEventBase):

    def setUp(self):
        super(TestRiskMatrix, self).setUp()

        self.context = self.user_model.context_get(self.cr, self.uid)
        cr, uid, context = self.cr, self.uid, self.context

        self.matrix_model = self.registry('mgmtsystem.risk.matrix')

        self.matrix_id = self.matrix_model.create(
            cr, uid, {
                'type': 'current',
                'system_id': self.system_id,
            }, context=context)

        self.matrix = self.matrix_model.browse(
            cr, uid, self.matrix_id, context=context)

        self.report = LocalService(
            'report.mgmtsystem_security_event.risk_matrix_webkit')

    def test_get_event_list(self):
        self.assertEqual(
            self.event.current_probability_id,
            self.get_probability(3, browse=True))

        self.assertEqual(
            self.event.current_severity_id,
            self.get_severity(3, browse=True))

        self.assertEqual(
            self.event_2.current_probability_id,
            self.get_probability(2, browse=True))

        self.assertEqual(
            self.event_2.current_severity_id,
            self.get_severity(2, browse=True))

        res = self.matrix.get_event_list(
            self.get_severity(3, browse=True),
            self.get_probability(3, browse=True))

        self.assertEqual(len(res), 1)

        res = self.matrix.get_event_list(
            self.get_severity(2, browse=True),
            self.get_probability(2, browse=True))

        self.assertEqual(len(res), 1)

        res = self.matrix.get_event_list(
            self.get_severity(3, browse=True),
            self.get_probability(2, browse=True))

        self.assertEqual(len(res), 0)

    def test_generate_risk_matrix_current(self):
        """
        Test that the risk matrix report is generated without error.
        """
        self.report.create(
            self.cr, self.uid, [self.matrix.id], {}, context=self.context)

    def test_generate_risk_matrix_original(self):
        """
        Test that the risk matrix report is generated without error \
        when the matrix type is original.
        """
        self.matrix.write({'type': 'original'})
        self.report.create(
            self.cr, self.uid, [self.matrix.id], {}, context=self.context)

    def test_generate_risk_matrix_residual(self):
        """
        Test that the risk matrix report is generated without error \
        when the matrix type is residual.
        """
        self.matrix.write({'type': 'residual'})
        self.report.create(
            self.cr, self.uid, [self.matrix.id], {}, context=self.context)
