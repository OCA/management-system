# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestModelCopyVerificationLines(common.TransactionCase):
    """Test wizard's method."""

    def test_copyVerificationLines(self):
        line_id = self.env["mgmtsystem.verification.line"].create(
            {
                "name": "What",
                "procedure_id": self.env.ref("document_page.demo_page1").id,
            }
        )

        src_record = self.env.ref("mgmtsystem_audit.mgmtsystem_audit_demo")
        src_record.line_ids = [line_id.id]
        dest_record = self.env.ref("mgmtsystem_audit.mgmtsystem_audit_demo2")
        copy_record = self.env["copy.verification.lines"].create(
            {"audit_src": src_record.id}
        )
        copy_record = copy_record.with_context(
            active_id=dest_record.id, active_model="mgmtsystem.audit"
        )

        copy_record.copyVerificationLines()

        self.assertGreater(len(dest_record.line_ids), 0)
