# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


def _parse_risk_formula(env, formula, a, b, c):
    """Calculate the risk replacing the variables A, B, C into the formula."""
    if not formula:
        raise UserError(
            env._(
                "You must define the company's risk computing formula. Go to settings"
            )
        )
    f = formula.replace("A", str(a)).replace("B", str(b)).replace("C", str(c))
    return safe_eval(f)
