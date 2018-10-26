from odoo import fields, models,  _


class MgmtsystemActionTag(models.Model):
    _name = "mgmtsystem.action.tag"
    _description = "Action Tags"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index', default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', _("Tag name already exists !")),
    ]
