# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import psycopg2

from odoo.addons.base.tests.common import BaseCommon


class TestModelAudit(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = cls.env.ref("document_page.demo_page1")
        cls.audit = cls.env["mgmtsystem.audit"].create(
            {
                "name": "Test audit",
                "date": "2025-01-01",
                "line_ids": [
                    (0, 0, {"name": "test", "procedure_id": cls.page.id}),
                    (0, 0, {"name": "test2"}),
                ],
            }
        )

    def test_get_action_url(self):
        """Test if action url start with http."""
        ret = self.audit.get_action_url()
        self.assertEqual(isinstance(ret, str), True)
        self.assertEqual(ret.startswith("http"), True)

    def test_button_close(self):
        """Test if button close change audit state to close."""
        self.audit.state = "open"
        self.assertEqual(self.audit.state, "open")
        self.audit.button_close()
        self.assertEqual(self.audit.state, "done")

    def test_get_lines_by_procedure(self):
        self.assertTrue(self.audit.get_lines_by_procedure())

    def test_copyVerificationLines(self):
        dest_record = self.env["mgmtsystem.audit"].create(
            {
                "name": "Test audit2",
                "date": "2025-01-01",
            }
        )
        copy_record = self.env["copy.verification.lines"].create(
            {"audit_src": self.audit.id}
        )
        copy_record = copy_record.with_context(
            active_id=dest_record.id, active_model=self.audit._name
        )
        copy_record.copyVerificationLines()
        self.assertGreater(len(dest_record.line_ids), 0)

    def test_audit_reports(self):
        res = self.env["ir.actions.report"]._render(
            "mgmtsystem_audit.audit_report_template", self.audit.ids
        )
        self.assertRegex(str(res[0]), "Test audit")
        res = self.env["ir.actions.report"]._render(
            "mgmtsystem_audit.verification_report_template", self.audit.ids
        )
        self.assertRegex(str(res[0]), "Test audit")

    def test_audit_tags(self):
        """Test that tags can be created and assigned to audits."""
        tag = self.env["mgmtsystem.audit.tag"].create(
            {"name": "Compliance", "color": 1}
        )
        self.assertTrue(tag.active)
        self.assertEqual(tag.color, 1)
        self.audit.tag_ids = tag
        self.assertIn(tag, self.audit.tag_ids)

    def test_audit_tag_unique_name(self):
        """Test that audit tag names must be unique."""
        self.env["mgmtsystem.audit.tag"].create({"name": "Duplicate"})
        with self.assertRaises(psycopg2.IntegrityError):
            self.env["mgmtsystem.audit.tag"].create({"name": "Duplicate"})
