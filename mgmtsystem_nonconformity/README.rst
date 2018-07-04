.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Management System - Nonconformity
=================================

This module enables you to manage the nonconformities of your management systems:

* Quality (ISO 9001)
* Environment (ISO 14001)
* Information Security (ISO 27001)
* Health and Safety (ISO 45001)
* IT Services (ISO 20000)

Installation
============

No installation required.

Configuration
=============

Users must be added to the appropriate groups within Odoo as follows:
* Creators: Settings > Users > Groups > Management System / User
To configure email notifications for certain stages go to:
* Management System > Configuration > Nonconformities > Stages
* Click on any stage and click the edit button.
* Click on the dropdown icon in the field Email Template, select your template and click Save. 

Usage
=====

To use this module:

* Go to Management System > Nonconformities
* Click on Create to enter the following information:

* Partner : Customer, supplier or internal personnel
* Related to: Any reference pointing to the NC (order id, project id, task id, etc.)
* Responsible: Person responsible for the NC
* Manager : Person managing the department or owner of the procedure
* Filled in by: Originator of NC report
* Origins:  The source of the NC, how was it discover
* Procedures:  Against which procedure is the NC
* Description: Evidence, reference to the standards

* Click on Save and then on Analysis.

Go to the newly created NC and fill in the following
information in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the results of the investigation
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on the Save button and then on the "Action Plan" button in the top right corner.

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

Enter comments into the input field below the "Plan Review" section, those comments are required to reach the next stage.

To begin the work on the planned Actions change the stage of the NC to open by clicking on the "In Progress" button in the top right corner.

When all actions of the plan are done, their effectiveness must be evaluated
before closing the NC.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/128/10.0

Known issues / Roadmap
======================

* The custom emails should be replaced by Mail Tracking features and Subtypes (like in Project Tasks and Project Issues)
* Automatically add responsible_user_id._uid, manager_user_id._uid, author_user_id._uid to chatter

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/Management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
Management-system/issues/new?body=module:%20
mgmtsystem_system%0Aversion:%20
10.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Daniel Reis <dreis.pt@hotmail.com>
* Glen Dromgoole <gdromgoole@tier1engineering.com>
* Loic Lacroix <loic.lacroix@savoirfairelinux.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>
* Eugen Don <eugen.don@don-systems.de>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
