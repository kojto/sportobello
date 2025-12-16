# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SportobelloAthleteOvertrainingTracker(models.Model):
    _name = 'sportobello.athlete.overtraining.tracker'
    _description = 'Overtraining Tracking'
    _rec_name = 'assessment_date'
    _order = 'assessment_date desc'

    athlete_id = fields.Many2one('sportobello.athletes', string='Athlete', required=True, ondelete='cascade')
    athlete_name = fields.Char(related='athlete_id.athlete_full_name', string='Athlete Name', readonly=True, store=True)
    assessment_date = fields.Date(string='Assessment Date', required=True, default=fields.Date.today)

    resting_heart_rate = fields.Float(string='RHR', digits=(10, 2), help='Resting Heart Rate - Resting heart rate in beats per minute (bpm)')
    heart_rate_recovery_1min = fields.Float(string='HRR 1min', digits=(10, 2), help='Heart Rate Recovery 1 minute - Heart rate drop after 1 minute in bpm')
    submaximal_exercise_heart_rate = fields.Float(string='Submax HR', digits=(10, 2), help='Submaximal Exercise Heart Rate - Heart rate at fixed load in bpm')

    countermovement_jump_height = fields.Float(string='CMJ', digits=(10, 2), help='Countermovement Jump - CMJ jump height in centimeters (cm)')
    sprint_time_trial = fields.Float(string='STT', digits=(10, 2), help='Sprint Time Trial - Sprint time or trial time in seconds (s)')

    blood_lactate_level = fields.Float(string='BLa', digits=(10, 2), help='Blood Lactate - Blood lactate level in mmol/L ×10 or μmol/L')

    grip_strength_left = fields.Float(string='GS L', digits=(10, 2), help='Grip Strength Left - Left hand strength in kg')
    grip_strength_right = fields.Float(string='GS R', digits=(10, 2), help='Grip Strength Right - Right hand strength in kg')

    notes = fields.Text(string='Notes', help='Additional notes for the assessment')

    @api.constrains('resting_heart_rate', 'heart_rate_recovery_1min', 'submaximal_exercise_heart_rate', 'countermovement_jump_height', 'sprint_time_trial', 'blood_lactate_level')
    def _check_measurements(self):
        for record in self:
            if record.resting_heart_rate and record.resting_heart_rate < 0:
                raise ValidationError(_('Resting heart rate cannot be negative'))
            if record.heart_rate_recovery_1min and record.heart_rate_recovery_1min < 0:
                raise ValidationError(_('Heart rate recovery cannot be negative'))
            if record.submaximal_exercise_heart_rate and record.submaximal_exercise_heart_rate < 0:
                raise ValidationError(_('Exercise heart rate cannot be negative'))
            if record.countermovement_jump_height and record.countermovement_jump_height < 0:
                raise ValidationError(_('Jump height cannot be negative'))
            if record.sprint_time_trial and record.sprint_time_trial < 0:
                raise ValidationError(_('Sprint time cannot be negative'))
            if record.blood_lactate_level and record.blood_lactate_level < 0:
                raise ValidationError(_('Lactate level cannot be negative'))
