# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SportobelloTrainingSessionCalendarLine(models.Model):
    _name = 'sportobello.training.session.lines'
    _description = 'Training Session Calendar Line'
    _order = 'sequence, id'

    calendar_id = fields.Many2one('sportobello.training.sessions', string='Calendar', required=True, ondelete='cascade')
    training_session_id = fields.Many2one('sportobello.training.session.elements', string='Training Element', required=True)
    training_session_description = fields.Text(related='training_session_id.description', string='Training Session Description', readonly=True)
    sequence = fields.Integer(string='Sequence', default=1)
