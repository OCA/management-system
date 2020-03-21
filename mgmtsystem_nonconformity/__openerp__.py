# -*- encoding: utf-8 -*-
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
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8
<<<<<<< df913a09410052efe02604e09f25e52d3005cf5f
    "name" : "Management System - Nonconformity",
    "version" : "1.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< ff56ec7c15f83ab383a3b19f8db21365dddbb53f
<<<<<<< 7ae63b3eb748c2c03907bd9e7a6ab8fb298c81df
    "license" : "AGPL-3",
=======
    "license" : "AGPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
=======
=======
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
    "name": "Management System - Nonconformity",
    "version": "1.2",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
<<<<<<< b9a32de449f11b9294519ef63ed8a1b78e6eb0f8
>>>>>>> [FIX] PEP8 compliance after running flake8
    "description": """\
This module enables you to manage the nonconformities of your management
system : quality (ISO9001), environment (ISO14001) or security (ISO27001).
=======
    "description": """\
This module enables you to manage the nonconformities of your management
system: quality (ISO9001), environment (ISO14001) or security (ISO27001).
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity

<<<<<<< ffd3c9212b4b83fa32ff295fbdbe999ad3ea2dfd
WARNING: when upgrading from v0.1, data conversion is required, since there are subtancial changes to the data structure.
=======
Configuration
=============

Users must be added to the appropriate groups within openERP as follows:
* Creators: Settings > Users > Groups > Management System / User
* Responsible Persons: Settings > Users > Groups > Management System / Approving User

Usage
=====

As a user, go to Management System > Nonconformities and click on Create to enter
the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC (order id, project id, task id, etc.)
* Responsible: Person responsible for the NC
* Manager : Person managing the department
* Filled in by: Originator of NC report
* Origins:  The source of the NC
* Procedures:  Against which procedure is the NC
* Description: Evidence, reference to standards

Click on Save and then on Send for Analysis.

As an approving user, go to the newly created NC and fill in the following information
in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the result of the investigation 
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on Approve and then on Send for Review.

In the Actions tab, select or create new actions by entering the following items:

* Subject: What must be done - Return to Supplier, Use As Is, Scrap, Rework, Re-grade, Repair
* Deadline: Date by which the action must be completed
* Responsible: Person in charge for implementing the action
* Type: Immediate, corrective or preventive actions or improvement opportunity
* Description: Details of the action

When the action is created, a notification is sent to the person responsible for the action. 

When the action plan is reviewed (comments) and approved, each action of the plan is opened.

When all actions of the plan are done, their effectiveness must be evaluated before closing
the NC.

Contributors
============

* Daniel Reis <dreis.pt@hotmail.com>
* Glen Dromgoole <gdromgoole@tier1engineering.com>
>>>>>>> [IMP] Documentation in the module description
    """,
    "depends": [
        'mgmtsystem_action',
        'document_page_procedure',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_nonconformity_security.xml',
        'mgmtsystem_nonconformity.xml',
        'mgmtsystem_nonconformity_workflow.xml',
        'nonconformity_sequence.xml',
        'board_mgmtsystem_nonconformity.xml',
        'mgmtsystem_nonconformity_data.xml',
    ],
    "demo": [
        'demo_nonconformity.xml',
    ],
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
