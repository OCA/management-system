from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestQuality(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "mgmtsystem.group_mgmtsystem_manager",
        "document_page.group_document_manager",
    )

    def test_quality_system_manual(self):
        system = self.env.ref("mgmtsystem_quality.system_quality")
        manual = self.env.ref(
            "document_page_quality_manual.document_page_quality_manual"
        )
        self.assertFalse(system.company_id)
        self.assertEqual(system.manual_id, manual)
        self.assertEqual(manual.type, "category")
        self.assertIn("Quality management system and its processes", manual.template)

    def test_quality_audit_and_review(self):
        system = self.env.ref("mgmtsystem_quality.system_quality")
        audit = self.env["mgmtsystem.audit"].create(
            {
                "name": "Quality system audit",
                "date": fields.Datetime.now(),
                "system_id": system.id,
            }
        )
        review = self.env["mgmtsystem.review"].create(
            {
                "name": "Quality system review",
                "date": fields.Datetime.now(),
                "system_id": system.id,
            }
        )
        self.assertEqual(audit.system_id, system)
        self.assertEqual(review.system_id, system)
        audit.button_close()
        review.button_close()
        self.assertEqual(audit.state, "done")
        self.assertEqual(review.state, "done")
