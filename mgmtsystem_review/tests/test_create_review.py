from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestModelReviewBase(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.review = cls.env["mgmtsystem.review"].create(
            {"name": "SampleReview", "date": fields.Datetime.now()}
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
