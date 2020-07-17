from odoo.tests.common import TransactionCase


class TestModelNonConformity(TransactionCase):

    def setUp(self):
        """
        Sets some enviroment
        """
        super(TestModelNonConformity, self).setUp()

        self.nc_model = self.env['mgmtsystem.nonconformity']

        self.nc = self.nc_model.search([])[0]
        self.nc['qty_checked'] = 100
        self.nc['qty_noncompliant'] = 50

    def test_nc(self):
        """
        Test NC changes
        """
        self.nc['qty_noncompliant'] = 150
        self.nc._onchange_qty_noncompliant()
        self.assertEqual(self.nc['qty_noncompliant'] == self.nc['qty_checked'], True)

        self.nc['qty_checked'] = 50
        self.nc._onchange_qty_checked()
        self.assertEqual(self.nc['qty_noncompliant'] == self.nc['qty_checked'], True)
