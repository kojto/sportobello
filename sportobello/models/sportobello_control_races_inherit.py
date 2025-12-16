# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class KojtoLandingpage(models.Model):
    _inherit = "kojto.landingpage"

    def open_sportobello_control_races_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_control_races").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }
