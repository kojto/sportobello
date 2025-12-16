# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SportobelloAthleteFunctionalTestTracker(models.Model):
    _name = 'sportobello.athlete.functional.test.tracker'
    _description = 'Functional Testing'
    _rec_name = 'test_date'
    _order = 'test_date desc'

    athlete_id = fields.Many2one('sportobello.athletes', string='Athlete', required=True, ondelete='cascade')
    athlete_name = fields.Char(related='athlete_id.athlete_full_name', string='Athlete Name', readonly=True, store=True)
    test_date = fields.Date(string='Test Date', required=True, default=fields.Date.today)

    # Heart Rate Metrics
    hr_max = fields.Integer(string='Max HR', help='Maximum heart rate in bpm. Used as reference to calculate heart rate zones.')
    hr_u2 = fields.Char(string='U2', compute='_compute_hr_zones', store=True, help='U2 zone (Utilisation 2). Low-intensity training, up to ~75% of Max HR.')
    hr_u1 = fields.Char(string='U1', compute='_compute_hr_zones', store=True, help='U1 zone (Mainly Utilisation). Moderate-intensity training, around ~80% of Max HR.')
    hr_at = fields.Char(string='AT', compute='_compute_hr_zones', store=True, help='AT zone (Anaerobic Threshold). High-intensity training, around ~85% of Max HR.')
    hr_t = fields.Char(string='T', compute='_compute_hr_zones', store=True, help='T zone (Transportation). Very high-intensity training, around ~95% of Max HR.')


    hr2 = fields.Integer(string='HR2', help='HR2 - Heart rate 2 minutes after test end')
    hr6 = fields.Integer(string='HR6', help='HR6 - Heart rate 6 minutes after test end')

    # VO2 Metrics
    vo2max = fields.Float(string='VO2max', digits=(10, 2), help='VO2max - Maximum oxygen capacity (ml/min)')
    vo2max_per_kg = fields.Float(string='VO2max/kg', digits=(10, 2), help='VO2max/kg - Maximum oxygen capacity per kilogram (ml/min/kg)')

    # Power Metrics
    w_max = fields.Float(string='MaxW', digits=(10, 2), help='MaxW (Maximum Power) - Maximum power (W)')
    w_max_per_kg = fields.Float(string='MaxW/kg', digits=(10, 2), help='MaxW/kg - Maximum power per kilogram (W/kg)')

    # Lactate Metrics
    la2 = fields.Float(string='La2', digits=(10, 2), help='La2 - Lactate 2 minutes after test end')
    la6 = fields.Float(string='La6', digits=(10, 2), help='La6 - Lactate 6 minutes after test end')
    la15 = fields.Float(string='La15', digits=(10, 2), help='La15 - Lactate 15 minutes after test end')

    # Other Metrics
    effective_pulse_zone = fields.Char(string='EPZ', help='Effective Pulse Zone - Effective pulse zone')
    rq1_per_w = fields.Float(string='RQ1/W', digits=(10, 2), help='RQ1/W - Respiratory quotient at 1W')

    notes = fields.Text(string='Notes', help='Additional notes for the test')

    @api.depends('hr_max')
    def _compute_hr_zones(self):
        """Calculate heart rate zones based on hr_max using training zone percentages:
        - U2 (Utilisation 2): 130-150 = Up to 75%
        - U1 (Mainly Utilisation): 140-160 = 80%
        - AT (Anaerobic Threshold): 150-170 = 85%
        - T (Transportation): 170-190 = 95%
        """
        for record in self:
            if not record.hr_max or record.hr_max <= 0:
                record.hr_u2 = False
                record.hr_u1 = False
                record.hr_at = False
                record.hr_t = False
                continue

            # Calculate zones based on percentages of hr_max
            # U2 (Utilisation 2): Up to 75% - range 130-150 (20 bpm range)
            hr_u2_center = int(record.hr_max * 0.75)
            hr_u2_from = hr_u2_center - 10
            hr_u2_to = hr_u2_center + 10
            record.hr_u2 = '%d-%d' % (hr_u2_from, hr_u2_to)

            # U1 (Mainly Utilisation): 80% - range 140-160 (20 bpm range)
            hr_u1_center = int(record.hr_max * 0.80)
            hr_u1_from = hr_u1_center - 10
            hr_u1_to = hr_u1_center + 10
            record.hr_u1 = '%d-%d' % (hr_u1_from, hr_u1_to)

            # AT (Anaerobic Threshold): 85% - range 150-170 (20 bpm range)
            hr_at_center = int(record.hr_max * 0.85)
            hr_at_from = hr_at_center - 10
            hr_at_to = hr_at_center + 10
            record.hr_at = '%d-%d' % (hr_at_from, hr_at_to)

            # T (Transportation): 95% - range 170-190 (20 bpm range)
            hr_t_center = int(record.hr_max * 0.95)
            hr_t_from = hr_t_center - 10
            hr_t_to = hr_t_center + 10
            record.hr_t = '%d-%d' % (hr_t_from, hr_t_to)

    @api.constrains('hr_max', 'vo2max', 'vo2max_per_kg', 'w_max', 'w_max_per_kg', 'rq1_per_w', 'la2', 'la6', 'la15', 'hr2', 'hr6')
    def _check_measurements(self):
        for record in self:
            if record.hr_max and record.hr_max < 0:
                raise ValidationError(_('Maximum heart rate cannot be negative'))
            if record.vo2max and record.vo2max < 0:
                raise ValidationError(_('VO2max cannot be negative'))
            if record.vo2max_per_kg and record.vo2max_per_kg < 0:
                raise ValidationError(_('VO2max/kg cannot be negative'))
            if record.w_max and record.w_max < 0:
                raise ValidationError(_('Maximum power cannot be negative'))
            if record.w_max_per_kg and record.w_max_per_kg < 0:
                raise ValidationError(_('MaxW/kg cannot be negative'))
            if record.rq1_per_w and record.rq1_per_w < 0:
                raise ValidationError(_('RQ1/W cannot be negative'))
            if record.la2 and record.la2 < 0:
                raise ValidationError(_('La2 cannot be negative'))
            if record.la6 and record.la6 < 0:
                raise ValidationError(_('La6 cannot be negative'))
            if record.la15 and record.la15 < 0:
                raise ValidationError(_('La15 cannot be negative'))
            if record.hr2 and record.hr2 < 0:
                raise ValidationError(_('HR2 cannot be negative'))
            if record.hr6 and record.hr6 < 0:
                raise ValidationError(_('HR6 cannot be negative'))
