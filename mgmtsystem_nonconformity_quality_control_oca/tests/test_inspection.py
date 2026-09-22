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
        cls.inspection_model = cls.env["qc.inspection"]
        inspection_lines = cls.inspection_model._prepare_inspection_lines(cls.test)
        cls.inspection1 = cls.inspection_model.create(
            {"name": "Test Inspection", "inspection_lines": inspection_lines}
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
