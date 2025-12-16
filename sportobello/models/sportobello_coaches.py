# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SportobelloCoaches(models.Model):
    _name = 'sportobello.coaches'
    _description = 'Sportobello Sport Club Coaches'
    _rec_name = 'full_name'

    sportsclub_id = fields.Many2one('sportobello', string='Sport Club', required=True, ondelete='cascade')

    active = fields.Boolean(string='Active', default=True)

    title = fields.Selection([
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
    ], string='Title', default='Mr')

    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', store=True, compute='_compute_full_name')

    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    specialization = fields.Char(string='Specialization')
    license_number = fields.Char(string='License Number')
    license_expiry_date = fields.Date(string='Valid Until')

    hire_date = fields.Date(string='Hire Date')

    @api.depends('title', 'first_name', 'middle_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            parts = []
            if record.title:
                parts.append(record.title)
            if record.first_name:
                parts.append(record.first_name)
            if record.middle_name:
                parts.append(record.middle_name)
            if record.last_name:
                parts.append(record.last_name)
            record.full_name = ' '.join(parts) if parts else ''
