# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class KojtoLandingpage(models.Model):
    _inherit = "kojto.landingpage"

    def open_sportobello_athletes_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_athletes").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_new_sportsclub_athlete_form(self):
        return {
            'name': _('New Athlete'),
            'type': 'ir.actions.act_window',
            'res_model': 'sportobello.athletes',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'context': {'create': True},
        }

    def open_sportobello_training_groups_list_view(self):
        action_id = self.env.ref("sportobello.action_sportobello_athlete_training_group").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_current_user_athlete_form(self):
        athlete = self.env['sportobello.athletes'].search([
            ('associated_user_id', '=', self.env.user.id)
        ], limit=1)

        if athlete:
            return {
                'name': _('My Athlete Profile'),
                'type': 'ir.actions.act_window',
                'res_model': 'sportobello.athletes',
                'res_id': athlete.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Athlete Profile'),
                    'message': _('No athlete profile is associated with your user account.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }
