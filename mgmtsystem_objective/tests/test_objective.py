# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, new_test_user


class TestObjective(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.system = cls.env["mgmtsystem.system"].create({"name": "Test System"})
        cls.user = new_test_user(
            cls.env, login="user_1", groups="mgmtsystem.group_mgmtsystem_user"
        )
        cls.objective = cls.env["mgmtsystem.objective"].create(
            {
                "name": "Test Objective",
                "system_id": cls.system.id,
                "user_id": cls.user.id,
            }
        )
        cls.indicator = cls.env["mgmtsystem.indicator"].create(
            {
                "name": "Test Indicator",
                "objective_id": cls.objective.id,
            }
        )

    def test_value(self):
        self.assertEqual(self.indicator.value, 0.0)
        value = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-01-01",
                "value": 100.0,
            }
        )
        self.assertEqual(self.indicator.value, 0.0)
        value.post()
        self.assertEqual(self.indicator.value, 100.0)
        value2 = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-02-01",
                "value": 200.0,
            }
        )
        self.assertEqual(self.indicator.value, 100.0)
        value2.post()
        self.assertEqual(self.indicator.value, 200.0)

    def test_value_security(self):
        with self.with_user(self.user.login):
            self.test_value()

    def test_value_no_access(self):
        self.objective.user_id = self.env.ref("base.user_root")
        with self.assertRaises(AccessError):
            self.env["mgmtsystem.indicator.value"].with_user(self.user.id).create(
                {
                    "indicator_id": self.indicator.id,
                    "date": "2024-01-01",
                    "value": 100.0,
                }
            )

    def test_state_no_target(self):
        self.assertEqual(self.indicator.value_state, "no_target")
        value = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-01-01",
                "value": 100.0,
            }
        )
        value.post()
        self.assertEqual(value.value_state, "no_target")
        self.assertEqual(self.indicator.value_state, "no_target")

    def test_state_below_target(self):
        self.indicator.has_min_target = True
        self.indicator.min_target_value = 150.0

        self.assertEqual(self.indicator.value_state, "no_target")
        value = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-01-01",
                "value": 100.0,
            }
        )
        value.post()
        self.assertEqual(value.value_state, "below_target")
        self.assertEqual(self.indicator.value_state, "below_target")

    def test_state_on_target(self):
        self.indicator.has_min_target = True
        self.indicator.min_target_value = 150.0
        self.assertEqual(self.indicator.value_state, "no_target")
        value = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-01-01",
                "value": 200.0,
            }
        )
        value.post()
        self.assertEqual(value.value_state, "on_target")
        self.assertEqual(self.indicator.value_state, "on_target")

    def test_state_above_target(self):
        self.indicator.has_max_target = True
        self.indicator.max_target_value = 250.0
        self.assertEqual(self.indicator.value_state, "no_target")
        value = self.env["mgmtsystem.indicator.value"].create(
            {
                "indicator_id": self.indicator.id,
                "date": "2024-01-01",
                "value": 300.0,
            }
        )
        value.post()
        self.assertEqual(value.value_state, "above_target")
        self.assertEqual(self.indicator.value_state, "above_target")
