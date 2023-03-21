from odoo.tests import common


class TestRepairOrder(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].create(
            {
                "name": "Product Test",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "uom_po_id": self.env.ref("uom.product_uom_unit").id,
            }
        )

        self.location_id = self.env["stock.location"].create(
            {
                "name": "Test Location",
                "usage": "internal",
                "location_id": self.env.ref("stock.stock_location_stock").id,
            }
        )

        self.repair_order = self.env["repair.order"].create(
            {
                "name": "Test Repair Order",
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
                "location_id": self.location_id.id,
            }
        )

        self.user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "testuser",
                "email": "testuser@example.com",
                "password": "password",
            }
        )

        self.user2 = self.env["res.users"].create(
            {
                "name": "Test User2",
                "login": "testuser2",
                "email": "testuser2@example.com",
                "password": "password",
            }
        )

        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

        self.request1 = self.env["mgmtsystem.nonconformity"].create(
            {
                "name": "Request 1",
                "partner_id": self.partner.id,
                "responsible_user_id": self.user.id,
                "manager_user_id": self.user2.id,
                "description": "desc1",
            }
        )

        self.request2 = self.env["mgmtsystem.nonconformity"].create(
            {
                "name": "Request 2",
                "partner_id": self.partner.id,
                "responsible_user_id": self.user.id,
                "manager_user_id": self.user2.id,
                "description": "desc1",
            }
        )

        self.repair_order.mgmtsystem_nonconformity_ids += self.request1
        self.repair_order.mgmtsystem_nonconformity_ids += self.request2

    def test_compute_mgmtsystem_nonconformity_count(self):
        self.repair_order._compute_mgmtsystem_nonconformity_count()
        assert self.repair_order.mgmtsystem_nonconformity_count == 2
