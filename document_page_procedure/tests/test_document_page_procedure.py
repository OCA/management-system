from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestDocumentPageProcedure(TransactionCase):
    def test_procedure_category_is_shared(self):
        category = self.env.ref("document_page_procedure.document_page_group_procedure")
        self.assertEqual(category.type, "category")
        self.assertFalse(category.company_id)

    def test_action_creates_procedure_from_template(self):
        action = self.env.ref("document_page_procedure.action_procedures")
        category = self.env.ref("document_page_procedure.document_page_group_procedure")
        Page = self.env[action.res_model].with_context(**safe_eval(action.context))
        with Form(Page, view="document_page.view_wiki_form") as form:
            form.name = "Quality procedure"
            form.draft_name = "1.0"
            form.draft_summary = "Initial procedure"
        procedure = form.record
        self.assertEqual(procedure.parent_id, category)
        for heading in (
            "Objective",
            "Application Domain",
            "Terms and Definitions",
            "Responsibilities",
            "Process",
        ):
            self.assertIn(heading, procedure.content)
        unrelated = self.env["document.page"].create({"name": "Other documentation"})
        procedures = Page.search(safe_eval(action.domain))
        self.assertIn(procedure, procedures)
        self.assertNotIn(unrelated, procedures)
