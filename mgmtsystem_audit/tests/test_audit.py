# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestModelAudit(common.TransactionCase):

    def test_get_action_url(self):
        """Test if action url start with http."""

        record = self.env.ref("mgmtsystem_audit.mgmtsystem_audit_demo")

        ret = record.get_action_url()

        self.assertEqual(isinstance(ret, basestring), True)
        self.assertEqual(ret.startswith('http'), True)

    def test_button_close(self):
        """Test if button close change audit state to close."""
        record = self.env.ref("mgmtsystem_audit.mgmtsystem_audit_demo")
        record.state = "open"
        self.assertEqual(record.state, "open")
        record.button_close()
        self.assertEqual(record.state, "done")

    def test_get_lines_by_procedure(self):
        line_id = self.env["mgmtsystem.verification.line"].create({
            "name": "test",
            "procedure_id": self.env.ref("document_page.demo_page1").id
        })
        line_id2 = self.env["mgmtsystem.verification.line"].create({
            "name": "test2",
        })

        record = self.env.ref("mgmtsystem_audit.mgmtsystem_audit_demo")
        record.line_ids = [line_id.id, line_id2.id]
        q = record.get_lines_by_procedure()
        self.assertTrue(q)
