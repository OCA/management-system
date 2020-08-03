##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Management System - Claim",
    "version": "13.0.1.1.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem", "crm_claim", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/mgmtsystem_claim_security.xml",
        "data/claim_sequence.xml",
        "data/mgmtsystem_claim_stage.xml",
        "data/email_template.xml",
        "data/automated_reminder.xml",
        "views/menus.xml",
        "views/mgmtsystem_claim.xml",
        "views/mgmtsystem_claim_stage.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
