# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestMgmtsystemReviewKpi(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = cls.env["kpi.category"].create({"name": "Test"})
        threshold_range = cls.env["kpi.threshold.range"].create(
            {
                "name": "OK",
                "min_type": "static",
                "max_type": "static",
                "min_fixed_value": 0,
                "max_fixed_value": 100,
                "color": "#00FF00",
            }
        )
        threshold = cls.env["kpi.threshold"].create(
            {
                "name": "Standard",
                "range_ids": [fields.Command.set([threshold_range.id])],
            }
        )
        cls.kpi1 = cls.env["kpi"].create(
            {
                "name": "KPI 1",
                "category_id": category.id,
                "threshold_id": threshold.id,
                "periodicity": 1,
                "periodicity_uom": "month",
            }
        )
        cls.kpi2 = cls.env["kpi"].create(
            {
                "name": "KPI 2",
                "category_id": category.id,
                "threshold_id": threshold.id,
                "periodicity": 1,
                "periodicity_uom": "month",
            }
        )
        cls.h1_jan = cls.env["kpi.history"].create(
            {
                "name": "KPI 1 - Jan",
                "kpi_id": cls.kpi1.id,
                "date": "2026-01-31 00:00:00",
                "value": 80.0,
                "color": "#00FF00",
            }
        )
        cls.h1_feb = cls.env["kpi.history"].create(
            {
                "name": "KPI 1 - Feb",
                "kpi_id": cls.kpi1.id,
                "date": "2026-02-28 00:00:00",
                "value": 85.0,
                "color": "#00FF00",
            }
        )
        cls.h2_jan = cls.env["kpi.history"].create(
            {
                "name": "KPI 2 - Jan",
                "kpi_id": cls.kpi2.id,
                "date": "2026-01-31 00:00:00",
                "value": 90.0,
                "color": "#00FF00",
            }
        )

    def test_create_autopopulates_kpi_history(self):
        """Creating a review auto-populates kpi_history_ids with latest
        history per KPI."""
        review = self.env["mgmtsystem.review"].create(
            {"name": "Test Review", "date": fields.Datetime.now()}
        )
        self.assertEqual(len(review.kpi_history_ids), 2)
        self.assertIn(self.h1_feb, review.kpi_history_ids)
        self.assertIn(self.h2_jan, review.kpi_history_ids)
        self.assertNotIn(self.h1_jan, review.kpi_history_ids)

    def test_create_no_kpi_history(self):
        """Creating a review with no KPI history leaves kpi_history_ids empty."""
        kpi3 = self.env["kpi"].create(
            {
                "name": "KPI no history",
                "category_id": self.kpi1.category_id.id,
                "threshold_id": self.kpi1.threshold_id.id,
                "periodicity": 1,
                "periodicity_uom": "month",
            }
        )
        self.assertFalse(kpi3.history_ids)
        review = self.env["mgmtsystem.review"].create(
            {"name": "No History Review", "date": fields.Datetime.now()}
        )
        self.assertNotIn(
            kpi3,
            review.kpi_history_ids.mapped("kpi_id"),
            "KPIs without history should not appear",
        )

    def test_button_update_kpi_history_at_review_date(self):
        """button_update_kpi_history picks latest history on or before review date."""
        review = self.env["mgmtsystem.review"].create(
            {"name": "Jan Review", "date": "2026-01-31 23:59:59"}
        )
        review.button_update_kpi_history()
        self.assertIn(self.h1_jan, review.kpi_history_ids)
        self.assertNotIn(self.h1_feb, review.kpi_history_ids)
        self.assertIn(self.h2_jan, review.kpi_history_ids)

    def test_button_update_kpi_history_after_date(self):
        """button_update_kpi_history includes Feb record when date is in March."""
        review = self.env["mgmtsystem.review"].create(
            {"name": "March Review", "date": "2026-03-31 23:59:59"}
        )
        review.button_update_kpi_history()
        self.assertIn(self.h1_feb, review.kpi_history_ids)
        self.assertNotIn(self.h1_jan, review.kpi_history_ids)
        self.assertIn(self.h2_jan, review.kpi_history_ids)
