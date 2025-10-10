# Copyright 2025 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common, tagged


@tagged("post_install", "-at_install")
class TestDocumentPage(common.TransactionCase):
    def setUp(self):
        super().setUp()
        if (
            "mgmtsystem.document" not in self.env
            or "document_page_id" not in self.env["mgmtsystem.document"]._fields
        ):
            self.skipTest("mgmtsystem module is not installed")

    def test_types(self):
        types = self.env["mgmtsystem.document"].get_document_types()
        self.assertIn("document", [t["id"] for t in types])

    def test_create_document(self):
        action = self.env["mgmtsystem.document"].add_element("document")
        with Form(
            self.env[action["res_model"]].with_context(**action["context"])
        ) as doc_form:
            doc_form.name = "SampleSystem"
        doc = doc_form.save()
        action = doc.action_create()
        rec = self.env[action["res_model"]].browse(action["res_id"])
        self.assertEqual(rec, doc.document_page_id)
        self.assertEqual(rec.name, "SampleSystem")
        rec.name = "ModifiedName"
        self.assertEqual(doc.name, "ModifiedName")
