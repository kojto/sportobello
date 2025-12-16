# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class KojtoLandingpage(models.Model):
    _inherit = "kojto.landingpage"

    def open_sportobello_coaches_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_coaches").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_sportobello_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello").id
        sportsclub = self.env['sportobello'].search([], limit=1)

        if sportsclub:
            url = f"/web#action={action_id}&id={sportsclub.id}&model=sportobello&view_type=form"
        else:
            url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_sportobello_training_sessions_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_training_sessions").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }


    def open_sportobello_training_sessions_list_readonly_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_training_sessions_readonly").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_sportobello_training_session_elements_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_training_session_elements").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }
