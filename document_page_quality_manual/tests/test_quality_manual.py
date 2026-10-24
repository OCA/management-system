from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestQualityManual(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "document_page.group_document_manager",
        "mgmtsystem.group_mgmtsystem_manager",
    )

    def test_quality_manual_category(self):
        category = self.env.ref(
            "document_page_quality_manual.document_page_quality_manual"
        )
        self.assertEqual(category.type, "category")
        self.assertFalse(category.company_id)
        self.assertIn("Context of the organization", category.template)
        self.assertIn("Continuous improvement", category.template)

    def test_create_manual_from_template(self):
        category = self.env.ref(
            "document_page_quality_manual.document_page_quality_manual"
        )
        with Form(self.env["document.page"]) as form:
            form.name = "Company quality manual"
            form.draft_name = "1.0"
            form.draft_summary = "Initial quality manual"
            form.parent_id = category
            self.assertEqual(form.content, category.template)
        manual = form.record
        self.assertEqual(manual.parent_id, category)
        self.assertEqual(manual.content, category.template)
        system = self.env["mgmtsystem.system"].create(
            {"name": "Quality management", "manual_id": manual.id}
        )
        self.assertEqual(system.manual_id, manual)
