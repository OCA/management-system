# Copyright 2012 Savoir-faire Linux <http://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user


class TestModelAction(common.TransactionCase):
    def test_create_system(self):
        record = self.env["mgmtsystem.system"].create({"name": "SampleSystem"})

        self.assertEqual(record.name, "SampleSystem")
        self.assertEqual(record.company_id.id, self.env.company.id)

    def test_viewer_readonly_and_manager_full_access(self):
        viewer = new_test_user(
            self.env,
            login="mgmtsystem_viewer_test",
            groups="mgmtsystem.group_mgmtsystem_viewer",
        )
        manager = new_test_user(
            self.env,
            login="mgmtsystem_manager_test",
            groups="mgmtsystem.group_mgmtsystem_manager",
        )
        system = (
            self.env["mgmtsystem.system"]
            .with_user(manager)
            .create({"name": "Managed system"})
        )
        self.assertEqual(system.with_user(viewer).name, "Managed system")
        with self.assertRaises(AccessError):
            self.env["mgmtsystem.system"].with_user(viewer).create({"name": "Denied"})
        with self.assertRaises(AccessError):
            system.with_user(viewer).write({"name": "Denied"})
        with self.assertRaises(AccessError):
            system.with_user(viewer).unlink()
        system.write({"name": "Updated system"})
        self.assertEqual(system.name, "Updated system")
        system.unlink()
        self.assertFalse(system.exists())

    def test_company_rule_keeps_shared_systems_visible(self):
        company = self.env.company
        other_company = self.env["res.company"].create({"name": "Other company"})
        manager = new_test_user(
            self.env,
            login="mgmtsystem_company_test",
            groups="mgmtsystem.group_mgmtsystem_manager",
            company_id=company.id,
            company_ids=[Command.set(company.ids)],
        )
        systems = self.env["mgmtsystem.system"].create(
            [
                {"name": "Own system", "company_id": company.id},
                {"name": "Shared system", "company_id": False},
                {"name": "Other system", "company_id": other_company.id},
            ]
        )
        visible = (
            systems.with_user(manager)
            .with_context(allowed_company_ids=company.ids)
            .search([("id", "in", systems.ids)])
        )
        self.assertEqual(set(visible.ids), set(systems[:2].ids))
        with self.assertRaises(AccessError):
            systems[2].with_user(manager).read(["name"])
