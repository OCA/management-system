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
            doc_form.kind = "procedure"
        doc = doc_form.save()
        action = doc.action_create()
        rec = self.env[action["res_model"]].browse(action["res_id"])
        self.assertEqual(rec, doc.document_page_id)
        self.assertEqual(rec.name, "SampleSystem")
        rec.name = "ModifiedName"
        self.assertEqual(doc.name, "ModifiedName")
        self.assertEqual(
            rec.parent_id,
            self.env.ref(
                "document_page_procedure.document_page_group_procedure",
            ),
        )
        rec.toggle_active()
        self.assertFalse(doc.active)
        rec.toggle_active()
        self.assertTrue(doc.active)

    def test_procedure_from_doc(self):
        doc = self.env["document.page"].create(
            {
                "name": "ProcedureDoc",
                "content": "<p>Content</p>",
            }
        )
        self.assertFalse(doc.mgmtsystem_document_procedure_ids)
        doc.toggle_procedure()
        self.assertEqual(len(doc.mgmtsystem_document_procedure_ids), 1)
        mgmtsystem_doc = doc.mgmtsystem_document_procedure_ids
        doc.toggle_procedure()
        doc.invalidate_recordset()
        self.assertFalse(mgmtsystem_doc.active)
        self.assertFalse(doc.mgmtsystem_document_procedure_ids)
        doc.toggle_procedure()
        doc.invalidate_recordset()
        self.assertTrue(mgmtsystem_doc.active)
        self.assertEqual(doc.mgmtsystem_document_procedure_ids, mgmtsystem_doc)
