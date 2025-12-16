# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SportobelloControlRaces(models.Model):
    _name = 'sportobello.control.races'
    _description = 'Sport Club Control Races'
    _rec_name = 'name'
    _order = 'date desc'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)

    control_race_type_id = fields.Many2one('sportobello.control.race.types', string='Type')
    control_race_measure = fields.Selection(related='control_race_type_id.control_race_measure', string='Measure Type', readonly=True)
    location = fields.Char(string='Location')

    measure_time = fields.Char(string='Time', help='Time in MM:SS format')
    measure_distance = fields.Float(string='Distance', digits=(10, 2), help='Distance in kilometers (e.g. 10.50 for 10.50km)')
    measure_repetitions = fields.Integer(string='Repetitions', help='Repetitions (e.g. 10 for 10 repetitions)')
    measure_strength = fields.Float(string='Strength', digits=(10, 2), help='Strength in kilograms (e.g. 100 for 100kg)')
    measure_height = fields.Float(string='Height', digits=(10, 2), help='Height in centimeters')
    measure_length = fields.Float(string='Length', digits=(10, 2), help='Length in meters')
    measure_heart_rate = fields.Integer(string='Heart Rate', help='Heart rate in beats per minute (e.g. 100 for 100bpm)')
    measure_other = fields.Char(string='Other', help='Other (e.g. "rating" for rating 10)')

    athlete_ids = fields.Many2many('sportobello.athletes', string='Athletes')

    def _format_time_value(self, value):
        if not value:
            return value

        digits = ''.join(filter(str.isdigit, str(value)))
        if not digits:
            return value

        digits = digits[-4:]
        digits = digits.zfill(4)

        minutes = digits[:-2]
        seconds = digits[-2:]
        return f"{minutes}:{seconds}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('measure_time') is not None:
                vals['measure_time'] = self._format_time_value(vals['measure_time'])
        return super().create(vals_list)

    def write(self, vals):
        if 'measure_time' in vals:
            vals['measure_time'] = self._format_time_value(vals['measure_time'])
        return super().write(vals)


class SportobelloControlRaceTypes(models.Model):
    _name = 'sportobello.control.race.types'
    _description = 'Sport Club Control Race Types'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    control_race_measure = fields.Selection([('time', "Time"), ('distance', "Distance"), ('repetitions', "Repetitions"), ('strength', "Strength / Weight"), ('height', "Height"), ('length', "Length"), ('heart_rate', "Heart Rate"), ('other', "Other")], string="Measurement Type", required=True)


class SportobelloAthletesControlRacesInherit(models.Model):
    _inherit = 'sportobello.athletes'

    control_races_ids = fields.Many2many('sportobello.control.races', string='Control Races')
