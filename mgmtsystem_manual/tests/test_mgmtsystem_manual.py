from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestMgmtsystemManual(TransactionCase):
    def test_manual_category_is_shared(self):
        category = self.env.ref("mgmtsystem_manual.manuals")
        self.assertEqual(category.type, "category")
        self.assertFalse(category.company_id)

    def test_system_manual_is_available_in_manuals_action(self):
        manual = self.env["document.page"].create(
            {
                "name": "Quality manual",
                "type": "content",
                "parent_id": self.env.ref("mgmtsystem_manual.manuals").id,
                "content": "<p>Quality management manual</p>",
            }
        )
        system = self.env["mgmtsystem.system"].create(
            {"name": "Quality management", "manual_id": manual.id}
        )
        other_category = self.env["document.page"].create(
            {"name": "Other documentation", "type": "category"}
        )
        other_page = self.env["document.page"].create(
            {
                "name": "Unrelated page",
                "type": "content",
                "parent_id": other_category.id,
            }
        )
        action = self.env.ref("mgmtsystem_manual.action_manuals")
        pages = self.env[action.res_model].search(safe_eval(action.domain))
        self.assertIn(system.manual_id, pages)
        self.assertNotIn(other_page, pages)
        self.assertEqual(
            system.manual_id.parent_id, self.env.ref("mgmtsystem_manual.manuals")
        )
