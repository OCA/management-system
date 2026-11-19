# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestResPartner(BaseCommon):
    _test_user_groups = ("base.group_partner_manager",)

    def test_quality_address_type(self):
        company = self.env["res.partner"].create(
            {"name": "Supplier", "is_company": True}
        )
        contact = self.env["res.partner"].create(
            {"name": "Quality manager", "parent_id": company.id, "type": "quality"}
        )
        self.assertEqual(contact.type, "quality")
        self.assertIn(contact, company.child_ids)
