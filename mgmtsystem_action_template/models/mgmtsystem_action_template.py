# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class MgmtsystemMgmEfficacy(models.Model):
    """
    Extend actions adding
    fields and method for template management
    """

    _inherit = 'mgmtsystem.action'

    # new fileds
    # template reference
    template_id = fields.Many2one(
        'mgmtsystem.action',
        'Reference Template',
        domain=[('is_template', '=', True)],
        default=False,
        help='Fill Action\'s fileds with Template\'s values'
        )
    # template flag
    is_template = fields.Boolean(
        'Template',
        help='Set Action as Template to create simlilar one. '
             'Type, Responsible, Tags and Title are used.'
        )

    # template description
    description_temp = fields.Html('Description preset')

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """
        fill some fields with template ones
        """

        if self.template_id.id:
            template = self.browse(self.template_id.id)

            self.name = _('NEW') + ' ' + template.name
            self.type_action = template.type_action
            self.description = template.description_temp
            self.user_id = template.user_id
            self.tag_ids = template.tag_ids

        return
