# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSecurityEventBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.system = cls.env["mgmtsystem.system"].create({"name": "Security System"})
        cls.probability_model = cls.env["mgmtsystem.risk.probability"]
        cls.severity_model = cls.env["mgmtsystem.risk.severity"]
        cls.vector_model = cls.env["mgmtsystem.security.vector"]
        cls.event_model = cls.env["mgmtsystem.security.event"]

        cls.probabilities = {
            value: cls.probability_model.create({"name": f"P{value}", "value": value})
            for value in range(1, 5)
        }
        cls.severities = {
            value: cls.severity_model.create({"name": f"S{value}", "value": value})
            for value in range(1, 5)
        }

        cls.vector = cls.vector_model.create(
            {
                "name": "S1",
                "original_probability_id": cls.probabilities[3].id,
                "original_severity_id": cls.severities[4].id,
                "current_probability_id": cls.probabilities[3].id,
                "current_severity_id": cls.severities[3].id,
                "residual_probability_id": cls.probabilities[1].id,
                "residual_severity_id": cls.severities[2].id,
                "system_id": cls.system.id,
            }
        )
        cls.vector_2 = cls.vector_model.create(
            {
                "name": "S2",
                "original_probability_id": cls.probabilities[4].id,
                "original_severity_id": cls.severities[4].id,
                "current_probability_id": cls.probabilities[2].id,
                "current_severity_id": cls.severities[2].id,
                "residual_probability_id": cls.probabilities[2].id,
                "residual_severity_id": cls.severities[1].id,
                "system_id": cls.system.id,
            }
        )
        cls.vector_3 = cls.vector_model.create(
            {
                "name": "S3",
                "original_probability_id": cls.probabilities[3].id,
                "original_severity_id": cls.severities[3].id,
                "current_probability_id": cls.probabilities[2].id,
                "current_severity_id": cls.severities[1].id,
                "residual_probability_id": cls.probabilities[2].id,
                "residual_severity_id": cls.severities[1].id,
                "system_id": cls.system.id,
            }
        )
        cls.event = cls.event_model.create(
            {
                "name": "E1",
                "type": "content",
                "system_id": cls.system.id,
                "scenario_ids": [
                    (0, 0, {"vector_id": cls.vector.id}),
                    (0, 0, {"vector_id": cls.vector_2.id}),
                ],
            }
        )
        cls.event_2 = cls.event_model.create(
            {
                "name": "E2",
                "type": "content",
                "system_id": cls.system.id,
                "scenario_ids": [
                    (0, 0, {"vector_id": cls.vector_2.id}),
                    (0, 0, {"vector_id": cls.vector_3.id}),
                ],
            }
        )


class TestCreateSecurityEvent(TestSecurityEventBase):
    def test_event_multi_field(self):
        self.assertEqual(self.event.original_probability_id, self.probabilities[4])
        self.assertEqual(self.event.original_severity_id, self.severities[4])
        self.assertEqual(self.event.current_probability_id, self.probabilities[3])
        self.assertEqual(self.event.current_severity_id, self.severities[3])
        self.assertEqual(self.event.residual_probability_id, self.probabilities[2])
        self.assertEqual(self.event.residual_severity_id, self.severities[2])

    def test_event_multi_field_change_value(self):
        self.vector.write(
            {
                "original_probability_id": self.probabilities[2].id,
                "original_severity_id": self.severities[2].id,
            }
        )
        self.vector_2.write(
            {
                "original_probability_id": self.probabilities[1].id,
                "original_severity_id": self.severities[1].id,
            }
        )
        self.event = self.event_model.browse(self.event.id)
        self.assertEqual(self.event.original_probability_id, self.probabilities[2])
        self.assertEqual(self.event.original_severity_id, self.severities[2])
