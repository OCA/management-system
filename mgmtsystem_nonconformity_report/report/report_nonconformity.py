############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2016 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
#    planned by: Sabrina Romero <sabrina@vauxoo.com>
############################################################################
from odoo import api, models


class MgmtsystemNonconformityReport(models.AbstractModel):
    _name = "report.mgmtsystem_nonconformity_report.nonconformity_report"

    @api.model
    def get_report_values(self, docids, data=None):
        nonconformity_obj = self.env['mgmtsystem.nonconformity']
        docs = nonconformity_obj.browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": 'mgmtsystem.nonconformity',
            "docs": docs,
            "data": data,
            "members_team": self._members_team,
            "get_part_name": self._get_part_name,
        }

    @api.multi
    def _members_team(self, nonconformity):
        """Return a list with the responsible, manager, author and users founds
        in the actions of this nonconformity, but not duplicates.
        """
        users = [nonconformity.responsible_user_id]
        if nonconformity.manager_user_id not in users:
            users.append(nonconformity.manager_user_id)
        if nonconformity.user_id not in users:
            users.append(nonconformity.user_id)
        for action in nonconformity.action_ids:
            if action.user_id not in users:
                users.append(action.user_id)
        return users

    @api.multi
    def _get_part_name(self, product, partner):
        """ If the product related to this nonconformity have seller_ids, and the
        partner related to the same nonconformity is found in this seller_ids
        will return the Supplier Product Name of this, else only will return
        the product description.
        """
        for seller in product.seller_ids:
            if seller.name.id == partner.id:
                return seller.product_name
        return product.description
