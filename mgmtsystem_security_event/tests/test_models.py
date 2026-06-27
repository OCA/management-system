# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestModelsBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.system = cls.env["mgmtsystem.system"].create({"name": "Test ISMS"})


class TestAssetCategory(TestModelsBase):
    def test_create(self):
        cat = self.env["mgmtsystem.security.asset.category"].create({"name": "Network"})
        self.assertEqual(cat.name, "Network")


class TestPrimaryAsset(TestModelsBase):
    def test_create(self):
        asset = self.env["mgmtsystem.security.asset.primary"].create(
            {
                "name": "ERP system",
                "description": "Main business application",
                "system_id": self.system.id,
            }
        )
        self.assertEqual(asset.name, "ERP system")
        self.assertEqual(asset.company_id, self.system.company_id)

    def test_responsible_user(self):
        user = self.env["res.users"].create(
            {"name": "Test User", "login": "test_responsible_user"}
        )
        asset = self.env["mgmtsystem.security.asset.primary"].create(
            {
                "name": "HR database",
                "system_id": self.system.id,
                "responsible_id": user.id,
            }
        )
        self.assertEqual(asset.responsible_id, user)


class TestSupportingAsset(TestModelsBase):
    def test_create_with_category(self):
        cat = self.env["mgmtsystem.security.asset.category"].create({"name": "Cloud"})
        asset = self.env["mgmtsystem.security.asset.supporting"].create(
            {
                "name": "Cloud storage",
                "system_id": self.system.id,
                "category_id": cat.id,
            }
        )
        self.assertEqual(asset.category_id, cat)
        self.assertEqual(asset.company_id, self.system.company_id)

    def test_link_primary_assets(self):
        primary = self.env["mgmtsystem.security.asset.primary"].create(
            {"name": "Financial data", "system_id": self.system.id}
        )
        supporting = self.env["mgmtsystem.security.asset.supporting"].create(
            {
                "name": "File server",
                "system_id": self.system.id,
                "primary_asset_ids": [(4, primary.id)],
            }
        )
        self.assertIn(primary, supporting.primary_asset_ids)


class TestThreatSource(TestModelsBase):
    def test_create(self):
        source = self.env["mgmtsystem.security.threat.source"].create(
            {"name": "Script kiddie", "system_id": self.system.id}
        )
        self.assertEqual(source.name, "Script kiddie")
        self.assertEqual(source.company_id, self.system.company_id)


class TestControl(TestModelsBase):
    def test_create(self):
        control = self.env["mgmtsystem.security.control"].create(
            {
                "name": "Firewall rules",
                "description": "Restrict inbound traffic.",
                "system_id": self.system.id,
            }
        )
        self.assertEqual(control.name, "Firewall rules")
        self.assertEqual(control.company_id, self.system.company_id)


class TestScenarioDisplayName(TestModelsBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        prob = cls.env["mgmtsystem.risk.probability"].create(
            {"name": "Low", "value": 1}
        )
        sev = cls.env["mgmtsystem.risk.severity"].create({"name": "Low", "value": 1})
        cls.vector = cls.env["mgmtsystem.security.vector"].create(
            {
                "name": "Phishing",
                "system_id": cls.system.id,
                "original_probability_id": prob.id,
                "original_severity_id": sev.id,
            }
        )
        cls.source = cls.env["mgmtsystem.security.threat.source"].create(
            {"name": "External attacker", "system_id": cls.system.id}
        )
        cls.event = cls.env["mgmtsystem.security.event"].create(
            {"name": "Credential theft", "type": "content", "system_id": cls.system.id}
        )

    def test_display_name_with_vector_and_source(self):
        scenario = self.env["mgmtsystem.security.event.scenario"].create(
            {
                "security_event_id": self.event.id,
                "vector_id": self.vector.id,
                "source_id": self.source.id,
            }
        )
        self.assertIn("Phishing", scenario.display_name)
        self.assertIn("External attacker", scenario.display_name)

    def test_display_name_without_source(self):
        scenario = self.env["mgmtsystem.security.event.scenario"].create(
            {"security_event_id": self.event.id, "vector_id": self.vector.id}
        )
        self.assertIn("Phishing", scenario.display_name)

    def test_display_name_without_vector_and_source(self):
        scenario = self.env["mgmtsystem.security.event.scenario"].create(
            {"security_event_id": self.event.id}
        )
        self.assertTrue(scenario.display_name)


class TestEventControlDisplayName(TestModelsBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.control = cls.env["mgmtsystem.security.control"].create(
            {"name": "Encryption", "system_id": cls.system.id}
        )
        cls.asset = cls.env["mgmtsystem.security.asset.supporting"].create(
            {"name": "Database server", "system_id": cls.system.id}
        )
        cls.event = cls.env["mgmtsystem.security.event"].create(
            {"name": "Data leak", "type": "content", "system_id": cls.system.id}
        )

    def test_display_name_full(self):
        line = self.env["mgmtsystem.security.event.control"].create(
            {
                "security_event_id": self.event.id,
                "control_id": self.control.id,
                "supporting_asset_id": self.asset.id,
            }
        )
        self.assertIn("Encryption", line.display_name)
        self.assertIn("Database server", line.display_name)

    def test_display_name_control_only(self):
        line = self.env["mgmtsystem.security.event.control"].create(
            {"security_event_id": self.event.id, "control_id": self.control.id}
        )
        self.assertIn("Encryption", line.display_name)

    def test_prevention_protection_recovery_flags(self):
        line = self.env["mgmtsystem.security.event.control"].create(
            {
                "security_event_id": self.event.id,
                "control_id": self.control.id,
                "prevention": True,
                "protection": False,
                "recovery": True,
            }
        )
        self.assertTrue(line.prevention)
        self.assertFalse(line.protection)
        self.assertTrue(line.recovery)


class TestRiskMatrixLevel(TestModelsBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["mgmtsystem.risk.matrix.level"].search([]).unlink()

    def test_overlapping_levels_raises(self):
        self.env["mgmtsystem.risk.matrix.level"].create(
            {
                "probability_min": 1,
                "probability_max": 2,
                "severity_min": 1,
                "severity_max": 2,
                "color": "green",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["mgmtsystem.risk.matrix.level"].create(
                {
                    "probability_min": 2,
                    "probability_max": 3,
                    "severity_min": 2,
                    "severity_max": 3,
                    "color": "orange",
                }
            )

    def test_non_overlapping_levels_ok(self):
        self.env["mgmtsystem.risk.matrix.level"].create(
            {
                "probability_min": 1,
                "probability_max": 2,
                "severity_min": 1,
                "severity_max": 1,
                "color": "green",
            }
        )
        level2 = self.env["mgmtsystem.risk.matrix.level"].create(
            {
                "probability_min": 1,
                "probability_max": 2,
                "severity_min": 2,
                "severity_max": 2,
                "color": "orange",
            }
        )
        self.assertTrue(level2.id)


class TestSecurityEventNoScenarios(TestModelsBase):
    def test_ratings_empty_when_no_scenarios(self):
        event = self.env["mgmtsystem.security.event"].create(
            {"name": "Orphan event", "type": "content", "system_id": self.system.id}
        )
        self.assertFalse(event.original_probability_id)
        self.assertFalse(event.original_severity_id)
        self.assertFalse(event.current_probability_id)
        self.assertFalse(event.current_severity_id)
        self.assertFalse(event.residual_probability_id)
        self.assertFalse(event.residual_severity_id)

    def test_ratings_clear_when_scenarios_removed(self):
        prob = self.env["mgmtsystem.risk.probability"].create(
            {"name": "High", "value": 4}
        )
        sev = self.env["mgmtsystem.risk.severity"].create({"name": "High", "value": 4})
        vector = self.env["mgmtsystem.security.vector"].create(
            {
                "name": "Test vector",
                "system_id": self.system.id,
                "original_probability_id": prob.id,
                "original_severity_id": sev.id,
            }
        )
        event = self.env["mgmtsystem.security.event"].create(
            {
                "name": "Temporary event",
                "type": "content",
                "system_id": self.system.id,
                "scenario_ids": [(0, 0, {"vector_id": vector.id})],
            }
        )
        self.assertTrue(event.original_probability_id)
        event.scenario_ids.unlink()
        self.assertFalse(event.original_probability_id)


class TestSecurityEventCIAFlags(TestModelsBase):
    def test_availability_only(self):
        event = self.env["mgmtsystem.security.event"].create(
            {
                "name": "Availability incident",
                "type": "content",
                "system_id": self.system.id,
                "confidentiality": False,
                "integrity": False,
                "availability": True,
            }
        )
        self.assertFalse(event.confidentiality)
        self.assertFalse(event.integrity)
        self.assertTrue(event.availability)

    def test_all_cia_flags(self):
        event = self.env["mgmtsystem.security.event"].create(
            {
                "name": "Full security incident",
                "type": "content",
                "system_id": self.system.id,
                "confidentiality": True,
                "integrity": True,
                "availability": True,
            }
        )
        self.assertTrue(event.confidentiality)
        self.assertTrue(event.integrity)
        self.assertTrue(event.availability)

    def test_integrity_only(self):
        event = self.env["mgmtsystem.security.event"].create(
            {
                "name": "Data tampering",
                "type": "content",
                "system_id": self.system.id,
                "confidentiality": False,
                "integrity": True,
                "availability": False,
            }
        )
        self.assertFalse(event.confidentiality)
        self.assertTrue(event.integrity)
        self.assertFalse(event.availability)
