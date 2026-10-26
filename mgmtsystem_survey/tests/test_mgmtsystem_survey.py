from odoo.addons.base.tests.common import BaseCommon


class TestMgmtsystemSurvey(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "mgmtsystem.group_mgmtsystem_manager",
        "survey.group_survey_manager",
    )

    def test_survey_menu_and_template(self):
        menu = self.env.ref("mgmtsystem_survey.menu_open_survey")
        self.assertIn(menu.id, self.env["ir.ui.menu"]._visible_menu_ids())
        action = self.env["ir.actions.actions"]._for_xml_id(
            "mgmtsystem_survey.action_survey_form"
        )
        survey = self.env.ref("mgmtsystem_survey.survey_customer_satisfaction")
        self.assertEqual(action["res_model"], survey._name)
        self.assertIn(survey, self.env[action["res_model"]].search([]))
        self.assertEqual(survey.access_mode, "public")
        self.assertEqual(survey.questions_layout, "page_per_section")
        self.assertTrue(survey.question_ids)

    def test_complete_customer_satisfaction_survey(self):
        survey = self.env.ref("mgmtsystem_survey.survey_customer_satisfaction")
        response = survey._create_answer(user=self.env.user, test_entry=True)
        for question in survey.question_ids:
            with self.subTest(question=question.title):
                if question.question_type == "scale":
                    answer = question.scale_max
                elif question.question_type in ("simple_choice", "multiple_choice"):
                    answer = question.suggested_answer_ids[0].id
                elif question.question_type == "matrix":
                    answer = {
                        row.id: [question.suggested_answer_ids[0].id]
                        for row in question.matrix_row_ids
                    }
                else:
                    self.assertEqual(question.question_type, "text_box")
                    answer = "Positive customer experience"
                response._save_lines(question, answer)
        response._mark_done()
        self.assertEqual(response.state, "done")
        self.assertEqual(response.user_input_line_ids.question_id, survey.question_ids)
        self.assertFalse(response.user_input_line_ids.filtered("skipped"))
        text_question = self.env.ref("mgmtsystem_survey.survey_cs_p5_q1")
        text_line = response.user_input_line_ids.filtered(
            lambda line: line.question_id == text_question
        )
        self.assertEqual(text_line.value_text_box, "Positive customer experience")
