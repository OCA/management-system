from odoo import Command
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestNonconformityHr(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "mgmtsystem.group_mgmtsystem_user",
        "document_knowledge.group_document_user",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env["hr.department"].create({"name": "Quality control"})
        cls.partner = cls.env["res.partner"].create({"name": "Quality customer"})
        cls.origin = cls.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "Department inspection"}
        )

    def test_department_in_nonconformity_form(self):
        with Form(self.env["mgmtsystem.nonconformity"]) as form:
            form.partner_id = self.partner
            form.manager_user_id = self.env.user
            form.responsible_user_id = self.env.user
            form.description = "Quality inspection finding"
            form.origin_ids.add(self.origin)
            form.department_id = self.department
        nonconformity = form.record
        self.assertEqual(nonconformity.department_id, self.department)
        with Form(nonconformity) as form:
            form.department_id = self.env["hr.department"]
        self.assertFalse(nonconformity.department_id)

    def test_nonconformity_without_department(self):
        nonconformity = self.env["mgmtsystem.nonconformity"].create(
            {
                "partner_id": self.partner.id,
                "manager_user_id": self.env.user.id,
                "responsible_user_id": self.env.user.id,
                "description": "General quality finding",
                "origin_ids": [Command.link(self.origin.id)],
            }
        )
        self.assertFalse(nonconformity.department_id)
        nonconformity.department_id = self.department
        self.assertEqual(nonconformity.department_id, self.department)
