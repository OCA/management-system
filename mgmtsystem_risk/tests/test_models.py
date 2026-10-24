# Copyright (C) 2025 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user


class TestRiskProbability(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

    def test_create(self):
        prob = self.env["mgmtsystem.risk.probability"].create(
            {"name": "Low", "value": 1}
        )
        self.assertEqual(prob.name, "Low")
        self.assertEqual(prob.value, 1)

    def test_default_company(self):
        prob = self.env["mgmtsystem.risk.probability"].create(
            {"name": "Medium", "value": 2}
        )
        self.assertEqual(prob.company_id, self.env.company)

    def test_description_optional(self):
        prob = self.env["mgmtsystem.risk.probability"].create(
            {"name": "High", "value": 3, "description": "Occurs frequently"}
        )
        self.assertEqual(prob.description, "Occurs frequently")

        prob_no_desc = self.env["mgmtsystem.risk.probability"].create(
            {"name": "Very High", "value": 4}
        )
        self.assertFalse(prob_no_desc.description)

    def test_multiple_levels(self):
        levels = [
            {"name": "L1", "value": 1},
            {"name": "L2", "value": 2},
            {"name": "L3", "value": 3},
        ]
        records = self.env["mgmtsystem.risk.probability"].create(levels)
        self.assertEqual(len(records), 3)
        self.assertEqual(records.mapped("value"), [1, 2, 3])


class TestRiskAccess(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.risk_user = new_test_user(
            cls.env,
            login="risk_readonly_test",
            groups="mgmtsystem.group_mgmtsystem_user",
        )
        cls.risk_manager = new_test_user(
            cls.env,
            login="risk_manager_test",
            groups="mgmtsystem.group_mgmtsystem_manager",
        )

    def test_user_readonly(self):
        for model in ("mgmtsystem.risk.probability", "mgmtsystem.risk.severity"):
            with self.subTest(model=model):
                level = self.env[model].create({"name": "Read-only level", "value": 1})
                level = level.with_user(self.risk_user)
                self.assertEqual(level.name, "Read-only level")
                with self.assertRaises(AccessError):
                    level.write({"value": 2})
                with self.assertRaises(AccessError):
                    self.env[model].with_user(self.risk_user).create(
                        {"name": "Forbidden level", "value": 2}
                    )
                with self.assertRaises(AccessError):
                    level.unlink()

    def test_manager_can_manage_levels(self):
        for model in ("mgmtsystem.risk.probability", "mgmtsystem.risk.severity"):
            with self.subTest(model=model):
                level = (
                    self.env[model]
                    .with_user(self.risk_manager)
                    .create({"name": "Managed level", "value": 1})
                )
                level.write({"value": 2})
                self.assertEqual(level.value, 2)
                level.unlink()
                self.assertFalse(level.exists())


class TestRiskSeverity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

    def test_create(self):
        sev = self.env["mgmtsystem.risk.severity"].create({"name": "Low", "value": 1})
        self.assertEqual(sev.name, "Low")
        self.assertEqual(sev.value, 1)

    def test_default_company(self):
        sev = self.env["mgmtsystem.risk.severity"].create(
            {"name": "Medium", "value": 2}
        )
        self.assertEqual(sev.company_id, self.env.company)

    def test_description_optional(self):
        sev = self.env["mgmtsystem.risk.severity"].create(
            {"name": "High", "value": 3, "description": "Major consequences"}
        )
        self.assertEqual(sev.description, "Major consequences")

        sev_no_desc = self.env["mgmtsystem.risk.severity"].create(
            {"name": "Critical", "value": 4}
        )
        self.assertFalse(sev_no_desc.description)

    def test_multiple_levels(self):
        levels = [
            {"name": "S1", "value": 1},
            {"name": "S2", "value": 2},
            {"name": "S3", "value": 3},
        ]
        records = self.env["mgmtsystem.risk.severity"].create(levels)
        self.assertEqual(len(records), 3)
        self.assertEqual(records.mapped("value"), [1, 2, 3])
