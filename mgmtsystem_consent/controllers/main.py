# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from werkzeug.exceptions import NotFound

from odoo.http import Controller, request, route


class ConsentController(Controller):
    @route("/consent/<any(accept,reject):choice>/"
           "<model('mgmtsystem.consent'):consent>/<token>",
           type="http", auth="public", website=True)
    def consent(self, choice, consent, token, *args, **kwargs):
        # TODO Add multi-db support
        consent = consent.sudo()
        if not (consent.exists() and consent._token() == token):
            raise NotFound
        consent.action_answer(choice == "accept")
        return request.render("mgmtsystem_consent.form", {
            "consent": consent,
        })
