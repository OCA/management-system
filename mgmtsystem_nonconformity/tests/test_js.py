# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo

from odoo.addons.web.tests.test_js import HOOTCommon, unit_test_error_checker


@odoo.tests.tagged("post_install", "-at_install")
class TestNonConformityFrontend(HOOTCommon):
    """Test Non Conformity OCA Frontend"""

    def get_hoot_filters(self):
        self._test_params = [("+", "@mgmtsystem_nonconformity")]
        return super().get_hoot_filters()

    @odoo.tests.no_retry
    def test_non_conformity(self):
        self.browser_js(
            f"/web/tests?headless&loglevel=2&preset=desktop&timeout=15000{self.hoot_filters}",
            "",
            "",
            login="admin",
            timeout=3600,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=unit_test_error_checker,
        )
