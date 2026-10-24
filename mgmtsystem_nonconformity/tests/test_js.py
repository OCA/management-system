# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo

from odoo.addons.web.tests.test_js import HootCommon, unit_test_error_checker


@odoo.tests.tagged("post_install", "-at_install")
class TestNonConformityFrontend(HootCommon):
    """Test Non Conformity OCA Frontend"""

    @odoo.tests.no_retry
    def test_non_conformity(self):
        self.browser_js(
            "/web/tests?headless&loglevel=2&preset=desktop&timeout=15000"
            "&filter=mgmtsystem_nonconformity",
            "",
            "",
            login="admin",
            timeout=180,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=unit_test_error_checker,
        )
