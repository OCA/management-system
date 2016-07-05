# -*- coding: utf-8 -*-
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
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
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
=======
    "name": "Management System - Nonconformity",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
<<<<<<< aedf771434404b2aa8c10c5f41955537a4c5e0cd
    "description": """\
This module enables you to manage the nonconformities of your management
system: quality (ISO9001), environment (ISO14001) or security (ISO27001).

>>>>>>> Moved mgmtsystem_nonconformity to root for port
Configuration
=============

Users must be added to the appropriate groups within openERP as follows:
* Creators: Settings > Users > Groups > Management System / User
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
* Responsible Persons: Settings > Users > Groups > Management System / Approving User
=======
* Responsible Persons:
  Settings > Users > Groups > Management System / Approving User
>>>>>>> Moved mgmtsystem_nonconformity to root for port

Usage
=====

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
As a user, go to Management System > Nonconformities and click on Create to enter
the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC (order id, project id, task id, etc.)
=======
As a user, go to Management System > Nonconformities and click on Create to
enter the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC
  (order id, project id, task id, etc.)
>>>>>>> Moved mgmtsystem_nonconformity to root for port
* Responsible: Person responsible for the NC
* Manager : Person managing the department
* Filled in by: Originator of NC report
* Origins:  The source of the NC
* Procedures:  Against which procedure is the NC
* Description: Evidence, reference to standards

Click on Save and then on Send for Analysis.

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
As an approving user, go to the newly created NC and fill in the following information
in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the result of the investigation 
=======
As an approving user, go to the newly created NC and fill in the following
informationi in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the result of the investigation
>>>>>>> Moved mgmtsystem_nonconformity to root for port
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on Approve and then on Send for Review.

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
In the Actions tab, select or create new actions by entering the following items:

* Subject: What must be done - Return to Supplier, Use As Is, Scrap, Rework, Re-grade, Repair
=======
In the Actions tab, select or create new actions by entering the following
items:

* Subject: What must be done - Return to Supplier, Use As Is, Scrap, Rework,
  Re-grade, Repair
>>>>>>> Moved mgmtsystem_nonconformity to root for port
* Deadline: Date by which the action must be completed
* Responsible: Person in charge for implementing the action
* Type: Immediate, corrective or preventive actions or improvement opportunity
* Description: Details of the action

<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
When the action is created, a notification is sent to the person responsible for the action. 

When the action plan is reviewed (comments) and approved, each action of the plan is opened.

When all actions of the plan are done, their effectiveness must be evaluated before closing
the NC.
=======
When the action is created, a notification is sent to the person responsible
for the action.

When the action plan is reviewed (comments) and approved, each action of the
plan is opened.

When all actions of the plan are done, their effectiveness must be evaluated
before closingi the NC.
>>>>>>> Moved mgmtsystem_nonconformity to root for port

Contributors
============

* Daniel Reis <dreis.pt@hotmail.com>
* Glen Dromgoole <gdromgoole@tier1engineering.com>
<<<<<<< 899847adfe25ce90522442c4414a01a83513b602
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
>>>>>>> [IMP] Documentation in the module description
=======
>>>>>>> Moved mgmtsystem_nonconformity to root for port
=======
* Loic Lacroix <loic.lacroix@savoirfairelinux.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
>>>>>>> Move datas to their own folders
    """,
=======
>>>>>>> mgmtsystem_nonconformity progress
    "depends": [
        'mgmtsystem_action',
        'document_page_procedure',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_nonconformity_security.xml',
        'views/mgmtsystem_nonconformity_state.xml',
        'views/mgmtsystem_nonconformity.xml',
        'views/mgmtsystem_origin.xml',
        'views/mgmtsystem_cause.xml',
        'views/mgmtsystem_severity.xml',
        'views/mgmtsystem_action.xml',
        'reports/mgmtsystem_nonconformity_report.xml',
        'data/sequence.xml',
        'data/mgmtsystem_nonconformity_severity.xml',
        'data/mgmtsystem_nonconformity_origin.xml',
        'data/mgmtsystem_nonconformity_cause.xml',
        'data/mgmtsystem_nonconformity_state.xml',
        'data/mail_message_subtype.xml',
    ],
    "demo": [
        "demo/mgmtsystem_nonconformity_origin.xml",
        "demo/mgmtsystem_nonconformity_cause.xml",
        "demo/mgmtsystem_nonconformity.xml",
    ],
<<<<<<< aedf771434404b2aa8c10c5f41955537a4c5e0cd
<<<<<<< 032a397f8f66a2977ac532de018235444c6316f6
<<<<<<< 71aa0a8a6f4f4f006d1786851185cfac782618dd
<<<<<<< 8a12276cf0affae66506dcba67980c75aac42247
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
    'installable': False,
=======
    'installable': True,
>>>>>>> Updated module as installable and removed depdencie on base_status
=======
    'installable': False,
>>>>>>> [MIG] Make modules uninstallable
=======
    'installable': True,
>>>>>>> mgmtsystem_nonconformity progress
}
>>>>>>> Moved mgmtsystem_nonconformity to root for port
