# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestModelNonConformity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nc_model = cls.env["mgmtsystem.nonconformity"]
        cls.partner = cls.env["res.partner"].search([])[0]
        cls.nc_test = cls.nc_model.create(
            {
                "partner_id": cls.partner.id,
                "manager_user_id": cls.env.user.id,
                "description": "description",
                "responsible_user_id": cls.env.user.id,
            }
        )
        action_vals = {"name": "An Action", "type_action": "immediate"}
        action1 = cls.nc_model.action_ids.create(action_vals)
        cls.nc_test.immediate_action_id = action1

    def test_stage_group(self):
        """Group by Stage shows all stages"""
        group_stages = self.nc_test.read_group(
            domain=[], fields=["stage_id"], groupby=["stage_id"]
        )
        num_stages = len(self.nc_model.stage_id.search([]))
        self.assertEqual(len(group_stages), num_stages)

    def test_reset_kanban_state(self):
        """Reset Kanban State on Stage change"""
        self.nc_test.kanban_state = "done"
        self.nc_test.stage_id = self.env.ref("mgmtsystem_nonconformity.stage_analysis")
        self.assertEqual(self.nc_test.kanban_state, "normal")

    def test_open_validation(self):
        """Don't allow approving/In Progress action comments"""
        open_stage = self.env.ref("mgmtsystem_nonconformity.stage_open")
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = open_stage

    def test_done_validation(self):
        """Don't allow closing an NC without evaluation comments"""
        done_stage = self.env.ref("mgmtsystem_nonconformity.stage_done")
        self.nc_test.action_comments = "OK!"
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = done_stage

    def test_done_actions_validation(self):
        """Don't allow closing an NC with open actions"""
        done_stage = self.env.ref("mgmtsystem_nonconformity.stage_done")
        self.nc_test.immediate_action_id.stage_id = self.env.ref(
            "mgmtsystem_action.stage_open"
        )
        self.nc_test.evaluation_comments = "OK!"
        with self.assertRaises(ValidationError):
            self.nc_test.stage_id = done_stage

    def test_state_transition(self):
        """Close and reopen Nonconformity"""
        self.nc_test.action_comments = "OK!"
        self.nc_test.stage_id = self.env.ref("mgmtsystem_nonconformity.stage_open")
        self.assertEqual(
            self.nc_test.immediate_action_id.stage_id,
            self.env.ref("mgmtsystem_action.stage_open"),
            "Plan Approval starts Actions",
        )

        self.nc_test.immediate_action_id.stage_id = self.env.ref(
            "mgmtsystem_action.stage_open"
        )
        self.nc_test.evaluation_comments = "OK!"
        self.nc_test.immediate_action_id.stage_id = self.env.ref(
            "mgmtsystem_action.stage_close"
        )
        self.nc_test.stage_id = self.env.ref("mgmtsystem_nonconformity.stage_done")
        self.assertEqual(self.nc_test.state, "done")
        self.assertTrue(self.nc_test.closing_date, "Set close date on Done")

        self.nc_test.stage_id = self.env.ref("mgmtsystem_nonconformity.stage_open")
        self.assertEqual(self.nc_test.state, "open")
        self.assertFalse(self.nc_test.closing_date, "Reset close date on reopen")
