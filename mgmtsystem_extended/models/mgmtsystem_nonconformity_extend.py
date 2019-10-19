# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class MgmtsystemMgmProduct(models.Model):
    """
    Extend nonconformity adding fields for type,
    quantity checked and quantity non compliant
    """

    # extended model
    _inherit = ['mgmtsystem.nonconformity']

    # new fields
    # nonconformity type
    nc_type = fields.Selection([('internal', 'Internal'),
                                ('supplier', 'Supplier'),
                                ('customer', 'Customer'),
                                ('external', 'External')
                                ],
                               'Type',
                               default='internal'
                               )
    # quantity checked to reveal the nonconformity [qty-ck]
    qty_checked = fields.Float('Quantity checked')
    # quantity found to be non-compliant with the inspection [qty-nc]
    qty_noncompliant = fields.Float('Quantity non-compliant')

    # define constraints for quantities

    @api.onchange('qty_noncompliant')
    def _onchange_qty_noncompliant(self):
        """
        set qty checked equal to qty non compliant if it is lower
        (qty-ck can not be lower to qty-nc)
        """
        if self.qty_noncompliant > self.qty_checked:
            self.qty_checked = self.qty_noncompliant

    @api.onchange('qty_checked')
    def _onchange_qty_checked(self):
        """
        set qty non compliant equal to qty checked if it is higher
        qty-nc can not be greater to qty-ck
        """
        if self.qty_checked < self.qty_noncompliant:
            self.qty_noncompliant = self.qty_checked


class MgmtsystemMgmEmail(models.Model):
    """
    Extend nonconformity adding method to send email
    """

    # extended model
    _inherit = ['mgmtsystem.nonconformity']

    # new method
    @api.multi
    def action_nc_sent(self):
        """
        send document to partner email
        if address not exists raises an error message
        """

        if self.partner_id.quality_contact_email:
            # find the e-mail template
            report_tmplt = self.env.ref(
                'mgmtsystem_extended.email_template_nonconformity')

            # send out the e-mail template to the partner
            self.env['mail.template'].browse(report_tmplt.id).send_mail(self.id)

        else:
            # raise an error
            raise models.ValidationError(
                _("The partner's quality contact email "
                  "is required in order to send the message.")
                )

        return


class MgmtsystemMgmTracking(models.Model):
    """
    Extend tracking on nonconformity field for Plan Review
    """

    # extended model
    _inherit = ['mgmtsystem.nonconformity']

    # add tracking
    action_comments = fields.Text(track_visibility='onchange')
