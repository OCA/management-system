from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestModelReviewBase(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "mgmtsystem.group_mgmtsystem_manager",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review = cls.env["mgmtsystem.review"].create(
            {"name": "SampleReview", "date": fields.Datetime.now()}
        )
        cls.other_company = cls.env["res.company"].create(
            {"name": "Other review company"}
        )
        cls.other_review = (
            cls.env["mgmtsystem.review"]
            .with_company(cls.other_company)
            .create({"name": "Other company review", "date": fields.Datetime.now()})
        )
        cls.other_line = (
            cls.env["mgmtsystem.review.line"]
            .with_company(cls.other_company)
            .create({"name": "Other company line", "review_id": cls.other_review.id})
        )


class TestModelReview(TestModelReviewBase):
    """Test class for mgmtsystem_review."""

    def test_review_misc(self):
        self.assertNotEqual(self.review.reference, "NEW")
        self.review.button_close()
        self.assertEqual(self.review.state, "done")
        res = self.env["ir.actions.report"]._render(
            "mgmtsystem_review.review_report_template", self.review.ids
        )
        self.assertRegex(str(res[0]), "SampleReview")

    def test_review_line_report(self):
        action = self.env["mgmtsystem.action"].create(
            {"name": "Review action", "type_action": "improvement"}
        )
        line = self.env["mgmtsystem.review.line"].create(
            {
                "name": "Review decision",
                "review_id": self.review.id,
                "type": "action",
                "action_id": action.id,
                "decision": "Improve quality procedures",
            }
        )
        self.assertIn(line, self.review.line_ids)
        html, _report_type = self.env["ir.actions.report"]._render_qweb_html(
            "mgmtsystem_review.review_report_template", self.review.ids
        )
        self.assertIn(b"Review action", html)
        self.assertIn(b"Improve quality procedures", html)

    def test_review_company_isolation(self):
        reviews = self.env["mgmtsystem.review"].search(
            [("id", "in", (self.review | self.other_review).ids)]
        )
        self.assertIn(self.review, reviews)
        self.assertNotIn(self.other_review, reviews)
        lines = self.env["mgmtsystem.review.line"].search(
            [("id", "=", self.other_line.id)]
        )
        self.assertFalse(lines)
