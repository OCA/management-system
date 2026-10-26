from odoo.addons.base.tests.common import BaseCommon


class TestMgmtsystemKpi(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "mgmtsystem.group_mgmtsystem_viewer",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = cls.env["kpi.category"].create({"name": "Quality indicators"})
        threshold = cls.env["kpi.threshold"].create({"name": "Quality threshold"})
        cls.kpi = cls.env["kpi"].create(
            {
                "name": "Quality performance",
                "category_id": category.id,
                "threshold_id": threshold.id,
                "kpi_type": "python",
                "kpi_code": "42.0",
            }
        )
        cls.kpi.compute_kpi_value()

    def test_viewer_can_see_kpi_menu(self):
        menu = self.env.ref("mgmtsystem_kpi.menu_mgmtsystem_kpi")
        self.assertIn(menu.id, self.env["ir.ui.menu"]._visible_menu_ids())

    def test_viewer_can_read_kpi_from_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("kpi.open_kpi_list")
        self.assertEqual(action["res_model"], "kpi")
        indicator = self.env[action["res_model"]].search([("id", "=", self.kpi.id)])
        self.assertEqual(indicator, self.kpi)
        self.assertEqual(indicator.value, 42.0)
        self.assertEqual(indicator.history_ids.value, 42.0)
