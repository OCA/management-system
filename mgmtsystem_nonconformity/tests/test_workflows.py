# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - present Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
from openerp.tests import common


class BreakSavePoint(Exception):
    pass


class TestModelNonConformity(common.TransactionCase):
    def setUp(self):
        super(TestModelNonConformity, self).setUp()
        self.partner_m = self.env['res.partner']
        self.conf_m = self.env['mgmtsystem.nonconformity']

        self.partner_obj = self.partner_m.search([])

    def try_states(self, obj, *methods):
        """
        Call multiple methods to check if we can move from
        one state to an other.
        """
        with self.cr.savepoint():
            for method in methods:
                with self.assertRaises(Exception):
                    getattr(obj, method)()
    
    def try_signal(self, obj, signal_name, state, rollback=False):
        """
        Try to trigger a signal.

        Then rollback to keep working on the same object. As
        if nothing happened.

        The savepoint get rolledback when there is an error.
        We use a custom error to catch when there is no error.
        And refresh the model to get back the changes from the
        database.
        """

        try:
            sid = self.cr.savepoint()
            with sid:
                obj.signal_workflow(signal_name)
                obj.refresh()
                self.assertEqual(obj.state, state)

                if rollback:
                    raise BreakSavePoint()
        except BreakSavePoint:
            obj.refresh()

    def try_cancel(self, obj):
        self.try_signal(obj, 'button_cancel', 'cancel', True)

    def try_invalid_signal(self, obj, signal_name, state):
        with self.assertRaises(Exception):
            self.try_signal(obj, signal_name, state, True)
    
    def test_workflow(self):

        conf_obj = self.conf_m.create({
            "manager_user_id": self.env.user.id,
            "partner_id": self.partner_obj[0].id,
            "description": "test",
            "responsible_user_id": self.env.user.id,
        })
        # Test draft
        self.assertEqual(conf_obj.state, 'draft')
        self.try_cancel(conf_obj)

        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_analysis()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_actions()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_evaluation()

        # Test draft to analysis
        # pending -> analysis
        self.try_invalid_signal(conf_obj, 'button_analysis_p', 'analysis')
        # analysis -> pending
        self.try_invalid_signal(conf_obj, 'button_review_n', 'pending')
        # open -> pending
        self.try_invalid_signal(conf_obj, 'button_review_p', 'pending')
        # pending-> open
        self.try_invalid_signal(conf_obj, 'button_open', 'open')
        # open -> done
        self.try_invalid_signal(conf_obj, 'button_close', 'done')
        # draft-> analysis
        # self.try_invalid_signal(conf_obj, 'button_analysis_n', 'analysis')
        self.try_signal(conf_obj, 'button_analysis_n', 'analysis')
        self.try_cancel(conf_obj)

        # Test Analysis to pending
        # pending -> analysis (already on analysis)
        self.try_signal(conf_obj, 'button_analysis_p', 'analysis')
        # draft-> analysis (already on analysis)
        self.try_signal(conf_obj, 'button_analysis_n', 'analysis')
        # analysis -> pending
        # self.try_invalid_signal(conf_obj, 'button_review_n', 'pending')
        # open -> pending
        self.try_invalid_signal(conf_obj, 'button_review_p', 'pending')
        # pending-> open
        self.try_invalid_signal(conf_obj, 'button_open', 'open')
        # open -> done
        self.try_invalid_signal(conf_obj, 'button_close', 'done')

        # Cannot go to pending as we didn't review
        self.try_invalid_signal(conf_obj, 'button_review_n', 'pending') 

        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_analysis()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_actions()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_evaluation()

        conf_obj.analysis = 'analysed'
        conf_obj.action_sign_analysis()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_evaluation()

        self.try_signal(conf_obj, 'button_review_n', 'pending') 
        self.try_cancel(conf_obj)

        # Test Pending to Open
        # pending -> analysis
        # self.try_invalid_signal(conf_obj, 'button_analysis_p', 'analysis')
        # draft-> analysis
        self.try_invalid_signal(conf_obj, 'button_analysis_n', 'analysis')
        # analysis -> pending
        self.try_signal(conf_obj, 'button_review_n', 'pending')
        # open -> pending
        self.try_signal(conf_obj, 'button_review_p', 'pending')
        # pending-> open
        #self.try_invalid_signal(conf_obj, 'button_open', 'open')
        # open -> done
        self.try_invalid_signal(conf_obj, 'button_close', 'done')

        self.try_invalid_signal(conf_obj, 'button_open', 'open')

        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_analysis()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_evaluation()

        conf_obj.action_sign_actions()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_actions()
        self.try_signal(conf_obj, 'button_open', 'open')

        # Test Open to Done
        # pending -> analysis
        self.try_invalid_signal(conf_obj, 'button_analysis_p', 'analysis')
        # draft-> analysis
        self.try_invalid_signal(conf_obj, 'button_analysis_n', 'analysis')
        # analysis -> pending
        self.try_invalid_signal(conf_obj, 'button_review_n', 'pending')
        # pending-> open
        self.try_signal(conf_obj, 'button_open', 'open')
        # open -> pending
        self.try_signal(conf_obj, 'button_review_p', 'pending', True)
        # open -> done
        self.try_invalid_signal(conf_obj, 'button_close', 'done')

        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_analysis()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                conf_obj.action_sign_actions()

        conf_obj.action_sign_evaluation()
        self.try_signal(conf_obj, 'button_close', 'done')
