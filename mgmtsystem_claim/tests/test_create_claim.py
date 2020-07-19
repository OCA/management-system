import time
from datetime import datetime, timedelta

import mock

from odoo.tests import common


def freeze_time(dt):
    mock_time = mock.Mock()
    mock_time.return_value = time.mktime(dt.timetuple())
    return mock_time


class TestModelClaim(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.claim = cls.env["mgmtsystem.claim"].create(
            {
                "name": "Test Claim",
                "team_id": cls.env.ref("sales_team.salesteam_website_sales").id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner Claim",
                "email": "partner.claim@example.com",
                "phone": "1234567890",
            }
        )
        cls.claim_categ = cls.env.ref("crm_claim.categ_claim1")
        cls.sales_team = cls.claim_categ.team_id

    def test_create_claim(self):
        self.assertNotEqual(self.claim.team_id, self.sales_team)
        self.assertTrue(self.claim.stage_id.id)
        self.claim.partner_id = self.partner
        self.claim.onchange_partner_id()
        self.assertEqual(self.claim.email_from, self.partner.email)
        self.assertEqual(self.claim.partner_phone, self.partner.phone)
        self.assertEqual(self.partner.mgmtsystem_claim_count, 1)
        self.claim.categ_id = self.claim_categ
        self.claim.onchange_categ_id()
        self.assertEqual(self.claim.team_id, self.sales_team)
        tmpl_model = self.env["mail.template"]
        with mock.patch.object(type(tmpl_model), "send_mail") as mocked:
            new_claim = self.claim.copy()
            new_claim.refresh()
            self.assertEqual(new_claim.stage_id.id, 1)
            self.assertIn("copy", new_claim.name)
            self.assertTrue(new_claim.stage_id.id)
            self.assertEqual(self.partner.mgmtsystem_claim_count, 2)
            mocked.assert_called_with(new_claim.id, force_send=True)

    def test_process_reminder_queue(self):
        """Check if process_reminder_queue work when days reminder are 10."""
        ten_days_date = datetime.now().date() + timedelta(days=10)
        self.claim.write(
            {
                "date_deadline": ten_days_date,  # 10 days from now
                "stage_id": self.env.ref("mgmtsystem_action.stage_open").id,
            }
        )
        with mock.patch("time.time", freeze_time(ten_days_date)):
            tmpl_model = self.env["mail.template"]
            with mock.patch.object(type(tmpl_model), "send_mail") as mocked:
                self.env["mgmtsystem.claim"].process_reminder_queue()
                mocked.assert_called_with(self.claim.id)

    def test_send_mail_for_action(self):
        """Check if send_mail_for_action work is called"""
        tmpl_model = self.env["mail.template"]
        with mock.patch.object(type(tmpl_model), "send_mail") as mocked:
            self.claim.send_mail_for_action(force_send=True)
            mocked.assert_called_with(self.claim.id, force_send=True)
