from odoo.tests import Form
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base.tests.common import BaseCommon


class TestWorkInstruction(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "document_page.group_document_manager",
        "mgmtsystem.group_mgmtsystem_manager",
    )

    def test_work_instruction_category(self):
        category = self.env.ref(
            "document_page_work_instruction.document_page_group_work_instructions"
        )
        self.assertEqual(category.type, "category")
        self.assertFalse(category.company_id)
        self.assertIn("Step 1", category.template)
        self.assertIn("Step 3", category.template)

    def test_create_instruction_from_menu_action(self):
        category = self.env.ref(
            "document_page_work_instruction.document_page_group_work_instructions"
        )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "document_page_work_instruction.work_instructions_action"
        )
        with Form(
            self.env[action["res_model"]].with_context(**safe_eval(action["context"]))
        ) as form:
            form.name = "Machine operating instructions"
            form.draft_name = "1.0"
            form.draft_summary = "Initial work instruction"
            self.assertEqual(form.parent_id, category)
            self.assertEqual(form.content, category.template)
        instruction = form.record
        self.assertEqual(instruction.content, category.template)
        unrelated = self.env["document.page"].create({"name": "Unrelated document"})
        visible_pages = self.env[action["res_model"]].search(
            safe_eval(action["domain"])
        )
        self.assertIn(instruction, visible_pages)
        self.assertNotIn(unrelated, visible_pages)
