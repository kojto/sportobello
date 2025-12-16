# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SportobelloTrainingSessionElements(models.Model):
    _name = 'sportobello.training.session.elements'
    _description = 'Sportobello Sport Club Training Session Elements'
    _rec_name = 'name'
    _order = 'create_date desc'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
    description_en = fields.Text(string='Description EN')
    note = fields.Text(string='Note')

