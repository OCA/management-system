# Copyright 2025 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common


class TestDocument(common.TransactionCase):
    def test_types(self):
        types = self.env["mgmtsystem.document"].get_document_types()
        self.assertIn("link", [t["id"] for t in types])

    def test_create_document(self):
        action = self.env["mgmtsystem.document"].add_element("link")
        with Form(
            self.env[action["res_model"]].with_context(**action["context"])
        ) as doc_form:
            doc_form.name = "SampleSystem"
            doc_form.link = "https://www.example.com"
        doc = doc_form.save()
        action = doc.action_create()
        self.assertEqual(doc.name, "SampleSystem")
        self.assertEqual(doc.link, "https://www.example.com")
        self.assertEqual(action["res_model"], doc._name)
        self.assertEqual(action["res_id"], doc.id)
