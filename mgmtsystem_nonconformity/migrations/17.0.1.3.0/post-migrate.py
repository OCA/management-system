# Copyright (C) 2026 Miquel Rosell <miquelrosell99@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Initializing mgmtsystem.nonconformity.date from create_date")
    cr.execute(
        """
        UPDATE mgmtsystem_nonconformity
        SET date = COALESCE(date, create_date)
        WHERE date IS NULL
        """
    )
