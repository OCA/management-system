from odoo import Command, fields
from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user


class TestHazard(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager = new_test_user(
            cls.env,
            login="hazard_manager_test",
            groups="mgmtsystem.group_mgmtsystem_manager",
        )
        cls.user = new_test_user(
            cls.env,
            login="hazard_user_test",
            groups="mgmtsystem.group_mgmtsystem_user",
        )
        cls.department = cls.env["hr.department"].create({"name": "Production"})
        cls.hazard_type = cls.env["mgmtsystem.hazard.type"].create({"name": "Physical"})
        cls.origin = cls.env["mgmtsystem.hazard.origin"].create({"name": "Machinery"})
        cls.category = cls.env["mgmtsystem.hazard.hazard"].create({"name": "Noise"})
        cls.hazard_values = {
            "name": "Machine noise exposure",
            "type_id": cls.hazard_type.id,
            "origin_id": cls.origin.id,
            "hazard_id": cls.category.id,
            "department_id": cls.department.id,
            "responsible_user_id": cls.manager.id,
            "analysis_date": fields.Date.today(),
        }

    def test_hazard_with_controls_and_tests(self):
        probability = self.env["mgmtsystem.risk.probability"].create(
            {"name": "Likely", "value": 3}
        )
        severity = self.env["mgmtsystem.risk.severity"].create(
            {"name": "High", "value": 3}
        )
        hazard = (
            self.env["mgmtsystem.hazard"]
            .with_user(self.manager)
            .create(
                {
                    **self.hazard_values,
                    "probability_id": probability.id,
                    "severity_id": severity.id,
                    "control_measure_ids": [
                        Command.create(
                            {
                                "name": "Hearing protection",
                                "responsible_user_id": self.manager.id,
                            }
                        )
                    ],
                    "test_ids": [
                        Command.create(
                            {
                                "name": "Noise measurement",
                                "responsible_user_id": self.manager.id,
                                "review_date": fields.Date.today(),
                            }
                        )
                    ],
                }
            )
        )
        self.assertEqual(hazard.probability_id, probability)
        self.assertEqual(hazard.severity_id, severity)
        measure = hazard.control_measure_ids
        test = hazard.test_ids
        self.assertEqual(measure.name, "Hearing protection")
        test.executed = True
        self.assertTrue(test.executed)
        hazard.unlink()
        self.assertFalse(measure.exists())
        self.assertFalse(test.exists())

    def test_user_permissions(self):
        hazard = (
            self.env["mgmtsystem.hazard"]
            .with_user(self.user)
            .create(self.hazard_values)
        )
        hazard.write({"justification": "Assessment updated"})
        self.assertEqual(hazard.justification, "Assessment updated")
        with self.assertRaises(AccessError):
            hazard.unlink()
        self.assertEqual(self.hazard_type.with_user(self.user).name, "Physical")
        with self.assertRaises(AccessError):
            self.hazard_type.with_user(self.user).write({"name": "Forbidden change"})

    def test_company_isolation(self):
        other_company = self.env["res.company"].create({"name": "Other hazard company"})
        foreign_hazard = self.env["mgmtsystem.hazard"].create(
            {**self.hazard_values, "company_id": other_company.id}
        )
        foreign_type = self.env["mgmtsystem.hazard.type"].create(
            {"name": "Foreign type", "company_id": other_company.id}
        )
        for record in (foreign_hazard, foreign_type):
            with self.subTest(model=record._name):
                visible = (
                    self.env[record._name]
                    .with_user(self.manager)
                    .search([("id", "=", record.id)])
                )
                self.assertFalse(visible)
