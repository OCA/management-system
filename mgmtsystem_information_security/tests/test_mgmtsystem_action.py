# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestMgmtSystemActionInformationSecurity(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.system = cls.env["mgmtsystem.system"].create(
            {
                "name": "Information Security",
                "company_id": cls.env.company.id,
            }
        )
        cls.action = cls.env["mgmtsystem.action"].create(
            {"name": "Test Action", "type_action": "immediate"}
        )
        cls.control = cls.env["mgmtsystem.security.control"].create(
            {
                "name": "Test Control",
                "system_id": cls.system.id,
            }
        )

    def test_link_security_controls(self):
        self.action.control_ids = self.control
        self.assertIn(self.control, self.action.control_ids)
