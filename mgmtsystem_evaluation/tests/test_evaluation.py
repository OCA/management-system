# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests.common import Form, TransactionCase


class TestEvaluation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.result_failed = cls.env["mgmtsystem.evaluation.result"].create(
            {"name": "Failed", "passed": False}
        )
        cls.result_passed = cls.env["mgmtsystem.evaluation.result"].create(
            {
                "name": "Passed",
                "passed": True,
            }
        )
        cls.template = cls.env["mgmtsystem.evaluation.template"].create(
            {
                "model_id": cls.env.ref("base.model_res_partner").id,
                "name": "Template",
                "feedback": "Feedback",
                "note": "Note",
                "result_ids": [(6, 0, (cls.result_failed | cls.result_passed).ids)],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Demo partner"})
        cls.partner_manager = cls.env["res.partner"].create(
            {"name": "Demo manager partner"}
        )
        cls.partner_manager_2 = cls.env["res.partner"].create(
            {"name": "Demo manager 2 partner"}
        )
        cls.user = cls.env["res.users"].create(
            {
                "partner_id": cls.partner.id,
                "login": "test_user_login",
                "password": "test_user_login",
            }
        )
        cls.manager = cls.env["res.users"].create(
            {
                "partner_id": cls.partner_manager.id,
                "login": "test_nanager_login",
                "password": "test_nanager_login",
            }
        )
        cls.manager_2 = cls.env["res.users"].create(
            {
                "partner_id": cls.partner_manager_2.id,
                "login": "test_nanager_login_2",
                "password": "test_nanager_login_2",
            }
        )
        cls.group = cls.env["res.groups"].create(
            {
                "name": "Group",
            }
        )
        cls.activity_1 = cls.env["mail.activity.type"].create({"name": "Activity 1"})
        cls.activity_2 = cls.env["mail.activity.type"].create({"name": "Activity 2"})

    def test_onchange(self):
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            self.assertFalse(f.feedback)
            f.template_id = self.template
            self.assertEqual(f.feedback, self.template.feedback)
            f.resource = self.partner

    def test_user(self):
        self.assertEqual(0, self.partner.mgmtsystem_evaluation_count)
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.manager_ids = self.manager
        self.assertFalse(evaluation.user_id)
        self.assertFalse(
            self.env["mgmtsystem.evaluation"]
            .with_user(self.user.id)
            .search([("id", "=", evaluation.id)])
        )
        evaluation.draft2progress()
        self.assertEqual(evaluation.user_id, self.user)
        self.assertEqual(
            evaluation,
            self.env["mgmtsystem.evaluation"]
            .with_user(self.user.id)
            .search([("id", "=", evaluation.id)]),
        )
        self.assertTrue(evaluation.with_user(self.manager).is_manager)
        self.assertFalse(evaluation.with_user(self.manager).is_user)
        self.assertFalse(
            self.env["mgmtsystem.evaluation"]
            .with_user(self.manager_2.id)
            .search([("id", "=", evaluation.id)]),
        )
        self.assertFalse(evaluation.with_user(self.user).is_manager)
        self.assertTrue(evaluation.with_user(self.user).is_user)
        self.assertEqual(1, self.partner.mgmtsystem_evaluation_count)

    def test_manager(self):
        self.assertEqual(0, self.partner.mgmtsystem_evaluation_count)
        self.group.users = self.manager_2
        self.template.group_id = self.group
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.manager_ids = self.manager
        self.assertFalse(evaluation.user_id)
        self.assertFalse(
            self.env["mgmtsystem.evaluation"]
            .with_user(self.user.id)
            .search([("id", "=", evaluation.id)])
        )
        evaluation.draft2progress()
        self.assertEqual(evaluation.user_id, self.user)
        self.assertEqual(
            evaluation,
            self.env["mgmtsystem.evaluation"]
            .with_user(self.user.id)
            .search([("id", "=", evaluation.id)]),
        )
        self.assertTrue(evaluation.with_user(self.manager).is_manager)
        self.assertFalse(evaluation.with_user(self.manager).is_user)
        self.assertTrue(evaluation.with_user(self.manager_2).is_manager)
        self.assertFalse(evaluation.with_user(self.manager_2).is_user)
        self.assertFalse(evaluation.with_user(self.user).is_manager)
        self.assertTrue(evaluation.with_user(self.user).is_user)
        self.assertEqual(1, self.partner.mgmtsystem_evaluation_count)

    def test_no_repetition(self):
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.draft2progress()
        evaluation.result_id = self.result_failed
        evaluation.progress2done()
        self.assertFalse(evaluation.next_evaluation_date)

    def test_repetition(self):
        self.template.write(
            {
                "recurrence_type": "monthly",
                "recurrence_period": 1,
            }
        )
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.draft2progress()
        evaluation.result_id = self.result_failed
        evaluation.progress2done()
        self.assertTrue(evaluation.next_evaluation_date)
        self.env["mgmtsystem.evaluation"]._cron_new_evaluation()
        self.assertFalse(
            self.env["mgmtsystem.evaluation"].search(
                [
                    ("template_id", "=", self.template.id),
                    ("id", "not in", evaluation.ids),
                ]
            )
        )
        with freeze_time(evaluation.next_evaluation_date):
            self.env["mgmtsystem.evaluation"]._cron_new_evaluation()
        self.assertTrue(
            self.env["mgmtsystem.evaluation"].search(
                [
                    ("template_id", "=", self.template.id),
                    ("id", "not in", evaluation.ids),
                ]
            )
        )

    def test_cancel_back_to_draft(self):
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.draft2progress()
        self.assertEqual("progress", evaluation.state)
        evaluation.cancel()
        self.assertEqual("cancel", evaluation.state)
        evaluation.back_to_draft()
        self.assertEqual("draft", evaluation.state)

    def test_activities(self):
        self.template.write(
            {
                "user_activity_type_id": self.activity_1.id,
                "manager_activity_type_id": self.activity_2.id,
            }
        )
        with Form(self.env["mgmtsystem.evaluation"]) as f:
            f.template_id = self.template
            f.resource = self.partner
        evaluation = f.save()
        evaluation.manager_ids = self.manager | self.manager_2
        self.assertFalse(evaluation.activity_ids)
        evaluation.draft2progress()
        self.assertEqual(3, len(evaluation.activity_ids))
        self.assertTrue(
            evaluation.activity_ids.filtered(
                lambda r: r.user_id == self.user
                and r.activity_type_id == self.activity_1
            )
        )
        self.assertTrue(
            evaluation.activity_ids.filtered(
                lambda r: r.user_id == self.manager
                and r.activity_type_id == self.activity_2
            )
        )
        self.assertTrue(
            evaluation.activity_ids.filtered(
                lambda r: r.user_id == self.manager_2
                and r.activity_type_id == self.activity_2
            )
        )
