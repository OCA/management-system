Management System - Nonconformity
=================================

This module enables you to manage the nonconformities of your management
system: quality (ISO9001), environment (ISO14001) or security (ISO27001).

Installation
============

To install this module, you need to:

* Clone the project from github on your instance
    * git clone https://github.com/OCA/management-system.git
* Start odoo with the project in the addons path

Configuration
=============

Users must be added to the appropriate groups within openERP as follows:
* Creators: Settings > Users > Groups > Management System / User
* Responsible Persons:
  Settings > Users > Groups > Management System / Approving User

Usage
=====

As a user, go to Management System > Nonconformities and click on Create to
enter the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC
  (order id, project id, task id, etc.)
* Responsible: Person responsible for the NC
* Manager : Person managing the department
* Filled in by: Originator of NC report
* Origins:  The source of the NC
* Procedures:  Against which procedure is the NC
* Description: Evidence, reference to standards

Click on Save and then on Send for Analysis.

As an approving user, go to the newly created NC and fill in the following
information in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the result of the investigation
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on Approve and then on Send for Review.

In the Actions tab, select or create new actions by entering the following
items:

* Subject: What must be done - Return to Supplier, Use As Is, Scrap, Rework,
  Re-grade, Repair
* Deadline: Date by which the action must be completed
* Responsible: Person in charge for implementing the action
* Type: Immediate, corrective or preventive actions or improvement opportunity
* Description: Details of the action

When the action is created, a notification is sent to the person responsible
for the action.

When the action plan is reviewed (comments) and approved, each action of the
plan is opened.

When all actions of the plan are done, their effectiveness must be evaluated
before closing the NC.

For further information, please visit:

 * https://github.com/OCA/management-system/issues

Known issues / Roadmap
======================

None

Credits
=======

Contributors
------------

* Daniel Reis <dreis.pt@hotmail.com>
* Glen Dromgoole <gdromgoole@tier1engineering.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
