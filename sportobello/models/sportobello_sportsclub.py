# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Sportobello(models.Model):
    _name = 'sportobello'
    _description = 'Sportobello Sport Club'
    _rec_name = 'name'

    name = fields.Char(string='Club Name', required=True)
    active = fields.Boolean(string='Active', default=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id, copy=False)

    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')

    coaches = fields.One2many('sportobello.coaches', 'sportsclub_id', string='Coaches')
