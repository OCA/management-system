.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Management Systems - Audit
==========================

This module was written to manage audits and verifications lists of your management system.

Installation
============

No installation required.

Configuration
=============

Users must be added to the appropriate groups within openERP as follows:

* Creators: Settings > Users > Groups > Management System / User
* Responsible Persons: Settings > Users > Groups > Management System / Approving User

Usage
=====

To use this module, you need to:

* go to Management Systems > Audits
* create a new audit
* fill up its name, its auditors and schedule the date
* prepare your questions with the verification list and print it
* drive the audit and log answers in your verification list
* finish your audit by writing the strong points, points to improve and creating improvements opportunities and nonconformities
* print the audit report and close the audit

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/128/10.0

For further information, please visit:

* http://fr.slideshare.net/max3903/iso-anmanagement-systemswithopenerpen

Known issues / Roadmap
======================

* None

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/management-system/issues/new?body=module:%20mgmtsystem_audit%0Aversion:%2010.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Daniel Reis <dreis.pt@hotmail.com>
* Joao Alfredo Gama Batista <joao.gama@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Virgil Dupras <virgil.dupras@savoirfairelinux.com>
* Loïc lacroix <loic.lacroix@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>
* Luk Vermeylen <luk@allmas-it.be>
* Maxime Chambreuil <mchambreuil@ursainfosystems.com>
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
