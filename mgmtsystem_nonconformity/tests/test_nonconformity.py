# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestModelNonConformity(common.TransactionCase):

    def setUp(self):
        super(TestModelNonConformity, self).setUp()
        self.nc_model = self.env['mgmtsystem.nonconformity']
        self.partner = self.env['res.partner'].search([])[0]
        self.nc_test = self.nc_model.create({
            'partner_id': self.partner.id,
            'manager_user_id': self.env.user.id,
            'description': "description",
            'responsible_user_id': self.env.user.id,
            })
        action_vals = {'name': 'An Action', 'type_action': 'correction'}
        action1 = self.nc_model.action_ids.create(action_vals)
        self.nc_test.corrective_action_id = action1

    def test_stage_group(self):
        """Group by Stage shows all stages"""
        group_stages = self.nc_test.read_group(
            domain=[],
            fields=['stage_id'],
            groupby=['stage_id'])
        num_stages = len(self.nc_model.stage_id.search([]))
        self.assertEqual(len(group_stages), num_stages)

    def test_reset_kanban_state(self):
        """Reset Kanban State on Stage change"""
        self.nc_test.kanban_state = 'done'
        self.nc_test.stage_id = \
            self.env.ref('mgmtsystem_nonconformity.stage_analysis')
        self.assertEqual(self.nc_test.kanban_state, 'normal')

    def test_open_validation(self):
        """Don't allow approving/In Progress action comments"""
        open_stage = self.env.ref('mgmtsystem_nonconformity.stage_open')
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = open_stage

    def test_done_validation(self):
        """Don't allow closing an NC without evaluation comments"""
        done_stage = self.env.ref('mgmtsystem_nonconformity.stage_done')
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = done_stage

    def test_done_actions_validation(self):
        """Don't allow closing an NC with open actions"""
        done_stage = self.env.ref('mgmtsystem_nonconformity.stage_done')
        self.nc_test.evaluation_comments = 'OK!'
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = done_stage

    def test_state_transition(self):
<<<<<<< e11781eb2f7f81e5285b3246d7bf45c8288b7893
        # Analysis
        # Test action_sign_analysis in non analysis mode
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)
        # Set analysis
        nonconformity.write({
            "state": "analysis",
        })
        # Test action_sign_analysis in analysis state and in non analysis mode
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Test action_sign_analysis  set analysis
        nonconformity.write({
            "analysis": "analysis test"
        })

        # Test transition to open state without action_sign_actions perform
        try:
            nonconformity.state = "open"
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Test transition to pending state without action_sign_analysis perform
        try:
            nonconformity.state = "pending"
        except exceptions.ValidationError:
            self.assertTrue(True)
        # perform action_sign_analysis
        nonconformity.action_sign_analysis()
        self.assertTrue(nonconformity.analysis_date)

        # Perform action_sign_analysis when it is already done
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Back to draft state when the object is not in cancel state
        try:
            nonconformity.state = "draft"
        except exceptions.ValidationError:
            self.assertTrue(True)
        # Cancel the object
        nonconformity.state = "cancel"
        self.assertTrue(nonconformity.cancel_date)

        # Done a cancel object
        try:
            nonconformity.state = "done"
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Bring to pending state a cancel object
        try:
            nonconformity.state = "pending"
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Reset the object
        nonconformity.state = "draft"
        self.assertFalse(nonconformity.analysis_date)
        self.assertFalse(nonconformity.actions_date)

        # Goto pending state
        nonconformity.write({
            "state": "analysis",
            "analysis": "analysis test"
        })

        # Sign action in non pending state
        try:
            nonconformity.action_sign_actions()
        except exceptions.ValidationError:
            self.assertTrue(True)

        nonconformity.action_sign_analysis()
        nonconformity.state = "pending"

        # Sign action in non open state
        try:
            nonconformity.action_sign_evaluation()
        except exceptions.ValidationError:
            self.assertTrue(True)

        analysis_date = nonconformity.analysis_date
        nonconformity.analysis_date = None
        # Sign action in non pending state
        try:
            nonconformity.action_sign_actions()
        except exceptions.ValidationError:
            self.assertTrue(True)
        nonconformity.analysis_date = analysis_date
        nonconformity.action_sign_actions()
        # Sign an already sign actions
        try:
            nonconformity.action_sign_actions()
        except exceptions.ValidationError:
            self.assertTrue(True)
        self.assertTrue(nonconformity.actions_date)
        actions = self.env["mgmtsystem.action"].search([])
        nonconformity.action_ids = actions[0]
        nonconformity.immediate_action_id = actions[1]
        nonconformity.state = "open"
        self.assertFalse(nonconformity.evaluation_date)

        # Done without closing immediate action
        try:
            nonconformity.state = "done"
        except exceptions.ValidationError:
            self.assertTrue(True)
        stage = nonconformity.immediate_action_id._get_stage_close()
        nonconformity.immediate_action_id.stage_id = stage
        # Done without closing actions
        try:
            nonconformity.state = "done"
        except exceptions.ValidationError:
            self.assertTrue(True)
        for action_id in nonconformity.action_ids:
            action_id.stage_id = stage
        # Done without signing evaluation
        try:
            nonconformity.state = "done"
        except exceptions.ValidationError:
            self.assertTrue(True)
        nonconformity.action_sign_evaluation()
        self.assertTrue(nonconformity.evaluation_date)

        # Done without the right to do it
        user_demo = self.browse_ref('base.user_demo')
        self.env = self.env(user=user_demo)
        nonconformity.state = "done"
        try:
            nonconformity.state = "done"
        except exceptions.ValidationError:
            self.assertTrue(True)
        # Switch to administrator before doing done
        self.env.user.sudo()
        nonconformity.state = "done"
        self.assertFalse(nonconformity._compute_age())
        self.assertFalse(nonconformity._compute_number_of_days_to_close())

        # cancel a close object
        try:
            nonconformity.state = "cancel"
        except exceptions.ValidationError:
            self.assertTrue(True)
        self.assertEqual(len(nonconformity._stage_groups(None, None)[0]), 6)
=======
        """Close and reopen Nonconformity"""
        self.nc_test.action_comments = 'OK!'
        self.nc_test.stage_id = self.env.ref(
            'mgmtsystem_nonconformity.stage_open')
        self.assertEqual(
            self.nc_test.corrective_action_id.stage_id,
            self.env.ref('mgmtsystem_action.stage_open'),
            'Plan Approval starts Actions')

        self.nc_test.evaluation_comments = 'OK!'
        self.nc_test.corrective_action_id.stage_id = \
            self.env.ref('mgmtsystem_action.stage_close')
        self.nc_test.stage_id = self.env.ref(
            'mgmtsystem_nonconformity.stage_done')
        self.assertEqual(self.nc_test.state, 'done')
        self.assertTrue(
            self.nc_test.closing_date, 'Set close date on Done')

        self.nc_test.stage_id = self.env.ref(
            'mgmtsystem_nonconformity.stage_open')
        self.assertEqual(self.nc_test.state, 'open')
<<<<<<< 560355a8b022a41103e49976945ee2467ab9fcfb
>>>>>>> Adjust tests and make them pass
=======
        self.assertFalse(
            self.nc_test.closing_date, 'Reset close date on reopen')
>>>>>>> Properly implement the NC closing date
