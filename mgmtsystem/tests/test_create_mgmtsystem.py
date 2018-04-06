# Copyright 2012 Savoir-faire Linux <http://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestModelAction(common.TransactionCase):

    def test_create_system(self):
        record = self.env['mgmtsystem.system'].create({
            "name": "SampleSystem",
        })

        self.assertEqual(record.name, "SampleSystem")
        self.assertEqual(record.company_id.id, self.env.user.company_id.id)
