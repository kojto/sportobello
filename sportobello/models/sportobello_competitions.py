# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SportobelloCompetitions(models.Model):
    _name = 'sportobello.competitions'
    _description = 'Sport Club Competitions'
    _rec_name = 'name'
    _order = 'date_start desc'

    name = fields.Char(string='Name', required=True)
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True)
    note = fields.Text(string='Note')

    participation_planned = fields.Boolean(string='Planned', default=False)
    participation_applied = fields.Boolean(string='Applied', default=False)
    participation_confirmed = fields.Boolean(string='Confirmed', default=False)

    athlete_ids = fields.Many2many('sportobello.athletes', string='Athletes')
    athlete_count = fields.Integer(string='Count', compute='_compute_athlete_count')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError(_('End date cannot be before start date.'))

    @api.depends('athlete_ids')
    def _compute_athlete_count(self):
        for record in self:
            record.athlete_count = len(record.athlete_ids)
