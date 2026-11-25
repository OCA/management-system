# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo

from odoo.addons.web.tests.test_js import WebSuite


@odoo.tests.tagged("post_install", "-at_install")
class TestMgmtSystemObjectiveSuite(WebSuite):
    """Test Automation OCA"""

    def get_hoot_filters(self):
        self._test_params = [("+", "@mgmtsystem_objective")]
        return super().get_hoot_filters()

    def test_mgmt_system_objective(self):
        self.test_unit_desktop()
