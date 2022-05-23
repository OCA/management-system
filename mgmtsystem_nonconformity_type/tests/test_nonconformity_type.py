from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestModelNonConformity(TransactionCase):
    def setUp(self):
        """
        Sets some enviroment
        """
        super(TestModelNonConformity, self).setUp()

        self.nc_model = self.env["mgmtsystem.nonconformity"]

        self.nc = self.nc_model.search([])[0]
        self.nc["qty_checked"] = 100
        self.nc["qty_noncompliant"] = 50

    def test_nc(self):
        """
        Test NC changes
        """
        self.nc["qty_noncompliant"] = 150
        self.nc._onchange_qty_noncompliant()
        self.assertEqual(self.nc["qty_noncompliant"] == self.nc["qty_checked"], True)

        self.nc["qty_checked"] = 50
        self.nc._onchange_qty_checked()
        self.assertEqual(self.nc["qty_noncompliant"] == self.nc["qty_checked"], True)

    def test_nc_email(self):
        """
        Test NC partner email
        """
        partner = self.nc.partner_id["child_ids"].search([])[0]
        partner_child = partner["child_ids"][0]
        partner_child.type = "quality"
        partner_child.email = "quality@example.com"
        self.nc.partner_id = partner.id

        self.assertEqual(True, self.nc.action_nc_sent())

        partner_child.type = "quality"
        partner_child.email = ""
        with self.assertRaises(ValidationError) as e:
            self.assertEqual(True, self.nc.action_nc_sent())
        self.assertIn(
            _(
                "The partner's quality contact email "
                "is required in order to send the message."
            ),
            str(e.exception),
        )
