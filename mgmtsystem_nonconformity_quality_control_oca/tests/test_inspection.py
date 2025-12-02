# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestQualityControl(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets some enviroment
        """
        super().setUpClass()
        cls.test = cls.env.ref("quality_control_oca.qc_test_1")
        cls.val_ok = cls.env.ref("quality_control_oca.qc_test_question_value_1")
        cls.inspection_model = cls.env["qc.inspection"]
        cls.inspection_lines = cls.inspection_model._prepare_inspection_lines(cls.test)
        cls.inspection1 = cls.inspection_model.create(
            {"name": "Test Inspection", "inspection_lines": cls.inspection_lines}
        )

        cls.product = cls.env["product.product"].create({"name": "Test product"})
        cls.inspection2 = cls.inspection_model.create(
            {
                "name": "Test Inspection 2",
                "inspection_lines": cls.inspection_lines,
                "object_id": cls.product,
            }
        )

        cls.nc_model = cls.env["mgmtsystem.nonconformity"]
        cls.partner = cls.env["res.partner"].search([])[0]
        cls.nc_test = cls.nc_model.create(
            {
                "partner_id": cls.partner.id,
                "manager_user_id": cls.env.user.id,
                "description": "description",
                "responsible_user_id": cls.env.user.id,
            }
        )
        cls.nc_test2 = cls.nc_model.create(
            {
                "partner_id": cls.partner.id,
                "manager_user_id": cls.env.user.id,
                "description": "description2",
                "responsible_user_id": cls.env.user.id,
            }
        )
        cls.inspection1.mgmtsystem_nonconformity_ids = [cls.nc_test.id]

    def test_compute_mgmtsystem_nonconformity_count(self):
        nc_count = len(self.inspection1.mgmtsystem_nonconformity_ids)
        self.inspection1._compute_mgmtsystem_nonconformity_count()
        self.assertEqual(nc_count, self.inspection1.mgmtsystem_nonconformity_count)

    def test_action_view_nonconformities(self):
        action = self.inspection1.action_view_nonconformities()
        self.assertEqual(self.nc_test.id, action["res_id"])

        self.inspection1.mgmtsystem_nonconformity_ids = [
            self.nc_test.id,
            self.nc_test2.id,
        ]
        action = self.inspection1.action_view_nonconformities()
        nc_ids = []
        for nc in self.inspection1.mgmtsystem_nonconformity_ids:
            nc_ids.append(nc.id)

        self.assertEqual(nc_ids, action["domain"][0][2])

    def test_no_create_nonconformity(self):
        """
        Test Nonconformity is not created when inspection
        fails with relative flag is off
        """
        self.inspection2.write({"state": "failed"})
        self.inspection2.action_approve()

        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "=", self.inspection2.id)]
        )
        self.assertFalse(nc)

    def test_create_nonconformity(self):
        """
        Test Nonconformity is created when inspection fails
        if relative flag is on
        """
        self.product.create_nonconformity = True
        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "=", self.inspection2.id)]
        )
        self.assertFalse(nc)
        self.inspection2.write({"state": "failed"})
        self.inspection2.action_approve()

        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "=", self.inspection2.id)]
        )
        self.assertEqual(len(nc), 1)
        self.assertEqual(self.inspection2.id, nc.qc_inspection_id.id)

    def test_create_nonconformity_with_no_product(self):
        self.inspection2.write({"state": "failed", "object_id": False})
        self.inspection2.action_approve()
        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "=", self.inspection2.id)]
        )
        self.assertFalse(nc)

    def test_create_nonconformity_with_multiple_inspections(self):
        self.product.create_nonconformity = True
        for line in self.inspection2.inspection_lines:
            if line.question_type == "qualitative":
                line.qualitative_value = self.val_ok
            if line.question_type == "quantitative":
                line.quantitative_value = 5.0
        self.inspection2.action_confirm()
        self.assertEqual(self.inspection2.state, "success")
        inspection3 = self.inspection_model.create(
            {
                "name": "Test Inspection 3",
                "inspection_lines": self.inspection_lines,
                "object_id": self.product,
            }
        )
        inspection3.write({"state": "failed"})
        multiple_inspections = inspection3 + self.inspection2
        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "in", (self.inspection2.id, inspection3.id))]
        )
        self.assertFalse(nc)
        multiple_inspections.action_approve()
        nc = self.env["mgmtsystem.nonconformity"].search(
            [("qc_inspection_id", "in", (self.inspection2.id, inspection3.id))]
        )
        self.assertEqual(len(nc), 1)
        self.assertEqual(inspection3.id, nc.qc_inspection_id.id)
