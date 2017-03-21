.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Management System - Nonconformity
=================================

This module enables you to manage the nonconformities of your management systems with pre defined workflows improving overall performance:

* ensure better data integrity and higher credibillity by sticking to a predefined and consistent workflow
* record occured nonconformities
* decide on actions based on data by analyzing and approving causes and origins of nonconformities
* increase yur proficiency for handling nonconformities by reviewing and approving the action plan for each nonconformitie (continuous cycle of improvement)
* improve your efficiency of dealing with nonconformities evaluating the progress on each action plan

Installation
============

No installation required.

Configuration
=============

The workflow approving Users must be added to the appropriate groups within Odoo as follows:
* Responsible (Approving) Persons: Settings > Users > Groups > Management System / Approving User

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

* Click on Save and then on Send for Analysis.

As an approving user, go to the newly created NC and fill in the following
information in the tab named Causes and Analysis:

* Causes: Add root causes
* Analysis: Describe the results of the investigation
* Severity: Select the severity among unfounded, minor and major
* Immediate action: Create or select an immediate action if appropriate

Click on Approve and then on Send for Action Planing.

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


Known issues / Roadmap
======================

* None

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
