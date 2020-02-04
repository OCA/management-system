# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MgmtsystemReview(models.Model):
    _name = "mgmtsystem.review"
    _inherit = ['mgmtsystem.review']
    
    employee_ids = fields.One2many('mgmtsystem.review.employee','review_id','employee_ids')
    partner_ids = fields.One2many('mgmtsystem.review.partner','review_id','partner_ids')
    
    def action_review_interne_sent(self):
        # if contact email exists send document
        # otherwise raises an error message

        for rec in self.employee_ids:

            if rec.employee_id.work_email and rec.presence :
                # find the e-mail template
                report_tmplt = self.env.ref('mgmtsystem_review_participant.email_template_interne_review')

                # send out the e-mail template to the employee
                self.env['mail.template'].browse(report_tmplt.id).send_mail(rec.id)

            else:
                # raise an error
                raise models.ValidationError(("The employee's email is required in order to send the message."))

    def action_review_externe_sent(self):
        # if contact email exists send document
        # otherwise raises an error message

        for rec in self.partner_ids:

            if rec.partner_id.notify_email and rec.presence:
                # find the e-mail template
                report_tmplt = self.env.ref('mgmtsystem_review_participant.email_template_externe_review')

                # send out the e-mail template to the partner
                self.env['mail.template'].browse(report_tmplt.id).send_mail(rec.id)

            else:
                # raise an error
                raise models.ValidationError(("The partner's email is required in order to send the message."))
            