# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestMgmtsystemActionNonconformity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.action = cls.env["mgmtsystem.action"].create(
            {
                "name": "Test Action",
                "type_action": "immediate",
            }
        )
        cls.nc = cls.env["mgmtsystem.nonconformity"].create(
            {
                "partner_id": cls.partner.id,
                "manager_user_id": cls.env.user.id,
                "responsible_user_id": cls.env.user.id,
                "description": "Test nonconformity",
            }
        )

    def test_nonconformity_count_no_nc(self):
        """An action without nonconformities counts 0."""
        self.assertEqual(self.action.nonconformity_count, 0)

    def test_nonconformity_count_with_nc(self):
        """Linking nonconformities increases the counter."""
        self.nc.action_ids = [(6, 0, self.action.ids)]
        self.assertEqual(self.action.nonconformity_count, 1)

    def test_action_open_nonconformities(self):
        """The smart button action returns the correct domain."""
        self.nc.action_ids = [(6, 0, self.action.ids)]
        result = self.action.action_open_nonconformities()
        self.assertEqual(result["res_model"], "mgmtsystem.nonconformity")
        self.assertEqual(
            result["domain"], [("id", "in", self.action.nonconformity_ids.ids)]
        )
