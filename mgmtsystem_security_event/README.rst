.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

=============
Feared Events
=============

This module allow you to manage feared events of your Information Security Management System (ISMS).

Installation
============

* No installation required.

Configuration
=============

You may customize the colors to be displayed on the risk matrix.

* go to Management System > Configuration > Security > Risk Matrix Levels

Define the colors related to a range of cells in the risk matrix.

Usage
=====

To use this module, you need to:

* go to Management System > Manuals > Security > Vectors

  - Create a scenario (S1)
  - Select the actual, original and residual probability and severity of the scenario

* go to Management System > Manuals > Security > Controls

  - Create a control (M1)

* go to Management System > Manuals > Security > Feared Events

  - Create a feared event (E1)
  - Add scenario S1 on the event
  - Add control M1 on the event

* go to Management System > Security > Risk Matrix

  - Select the type of matrix to generate and click on 'Done'

Credits
=======

Contributors
------------

* Loïc Faure-Lacroix <loic.lacroix@savoirfairelinux.com>
* David Dufresne <david.dufresne@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
* Nicolas Zin <nicolas.zin@savoirfairelinux.com>

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
