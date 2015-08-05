.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Management Systems - Nonconformity Claim
========================================

This module was written to extend the nonconformity form so it can also represent 
NC candidates and other types of feedback, such as complaints, measurements, suggestions, etc.

The "type" field identifies if the feedback corresponds to a nonconformity, or
to other type of record, such as "best practice", "suggestion", etc.

This module purpose overlaps with "mgmtsystem_claim" module, so you should use
either one or the other.

It will fit best to your uses cases requiring:
  * a common numbering sequence for complaints and nonconformities;
  * a single point-of-entry for all management system related occurrences.

Usage
=====

To use this module, you need to:

* go to Management Systems >  Nonconformities

`Try it live! <https://runbot.odoo-community.org/runbot/128/8.0>`_

For further information, please visit:

* https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

* None

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/management-system/issues/new?body=module:%20mgmtsystem_nonconformity_claim%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Daniel Reis <dreis.pt@gmail.com>
* Loïc Lacroix <loic.lacroix@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>

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
