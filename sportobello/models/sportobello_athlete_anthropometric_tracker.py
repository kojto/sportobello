# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SportobelloAthleteAnthropometricTracker(models.Model):
    _name = 'sportobello.athlete.anthropometric.tracker'
    _description = 'Anthropometric Tracker'
    _rec_name = 'assessment_date'
    _order = 'assessment_date desc'

    athlete_id = fields.Many2one('sportobello.athletes', string='Athlete', required=True, ondelete='cascade')
    athlete_name = fields.Char(related='athlete_id.athlete_full_name', string='Athlete Name', readonly=True, store=True)
    assessment_date = fields.Date(string='Assessment Date', required=True, default=fields.Date.today)

    # Basic Measurements
    height = fields.Float(string='Height', digits=(10, 2), help='Height - Height in centimeters (cm)')
    weight = fields.Float(string='Weight', digits=(10, 2), help='Weight - Weight in kilograms (kg)')
    bmi = fields.Float(string='BMI', digits=(10, 2), compute='_compute_bmi', store=True, help='BMI')

    # Body Dimensions
    wingspan = fields.Float(string='Wingspan', digits=(10, 2), help='Wingspan - Wingspan in centimeters (cm)')
    arm_length_left = fields.Float(string='Arm L L', digits=(10, 2), help='Arm Length Left - Left arm length in centimeters (cm)')
    arm_length_right = fields.Float(string='Arm L R', digits=(10, 2), help='Arm Length Right - Right arm length in centimeters (cm)')
    leg_length_left = fields.Float(string='Leg L L', digits=(10, 2), help='Leg Length Left - Left leg length in centimeters (cm)')
    leg_length_right = fields.Float(string='Leg L R', digits=(10, 2), help='Leg Length Right - Right leg length in centimeters (cm)')
    shoulder_width = fields.Float(string='Shoulder W', digits=(10, 2), help='Shoulder Width - Shoulder width in centimeters (cm)')

    # Circumferences
    chest_circumference = fields.Float(string='Chest C', digits=(10, 2), help='Chest Circumference - Chest circumference in centimeters (cm)')
    waist_circumference = fields.Float(string='Waist C', digits=(10, 2), help='Waist Circumference - Waist circumference in centimeters (cm)')
    hip_circumference = fields.Float(string='Hip C', digits=(10, 2), help='Hip Circumference - Hip circumference in centimeters (cm)')
    neck_circumference = fields.Float(string='Neck C', digits=(10, 2), help='Neck Circumference - Neck circumference in centimeters (cm)')
    bicep_circumference_left = fields.Float(string='Bicep C L', digits=(10, 2), help='Bicep Circumference Left - Left bicep circumference in centimeters (cm)')
    bicep_circumference_right = fields.Float(string='Bicep C R', digits=(10, 2), help='Bicep Circumference Right - Right bicep circumference in centimeters (cm)')
    thigh_circumference_left = fields.Float(string='Thigh C L', digits=(10, 2), help='Thigh Circumference Left - Left thigh circumference in centimeters (cm)')
    thigh_circumference_right = fields.Float(string='Thigh C R', digits=(10, 2), help='Thigh Circumference Right - Right thigh circumference in centimeters (cm)')
    calf_circumference_left = fields.Float(string='Calf C L', digits=(10, 2), help='Calf Circumference Left - Left calf circumference in centimeters (cm)')
    calf_circumference_right = fields.Float(string='Calf C R', digits=(10, 2), help='Calf Circumference Right - Right calf circumference in centimeters (cm)')

    # Body Composition
    body_fat_percentage = fields.Float(string='BF%', digits=(10, 2), help='Body Fat Percentage - Body fat (%)')
    muscle_mass = fields.Float(string='MM', digits=(10, 2), help='Muscle Mass - Muscle mass in kilograms (kg)')
    bone_mass = fields.Float(string='BM', digits=(10, 2), help='Bone mass in kg')
    water_percentage = fields.Float(string='Water%', digits=(10, 2), help='Water Percentage - Water percentage (%)')
    visceral_fat = fields.Float(string='VF', digits=(10, 2), help='Visceral Fat - Visceral fat')

    # Additional Measurements
    sitting_height = fields.Float(string='Sitting Ht', digits=(10, 2), help='Sitting Height - Sitting height in centimeters (cm)')
    reach_height = fields.Float(string='Reach Ht', digits=(10, 2), help='Reach Height - Reach height in centimeters (cm)')
    hand_length_left = fields.Float(string='Hand L L', digits=(10, 2), help='Hand Length Left - Left hand length in centimeters (cm)')
    hand_length_right = fields.Float(string='Hand L R', digits=(10, 2), help='Hand Length Right - Right hand length in centimeters (cm)')
    foot_length_left = fields.Float(string='Foot L L', digits=(10, 2), help='Foot Length Left - Left foot length in centimeters (cm)')
    foot_length_right = fields.Float(string='Foot L R', digits=(10, 2), help='Foot Length Right - Right foot length in centimeters (cm)')

    # Notes
    notes = fields.Text(string='Notes', help='Additional notes for the assessment')

    @api.depends('height', 'weight')
    def _compute_bmi(self):
        for record in self:
            if record.height and record.weight and record.height > 0:
                # BMI = weight (kg) / (height (m))^2
                height_in_meters = record.height / 100.0
                record.bmi = record.weight / (height_in_meters ** 2)
            else:
                record.bmi = 0.0

    @api.constrains('height', 'weight', 'bmi')
    def _check_measurements(self):
        for record in self:
            if record.height and record.height < 0:
                raise ValidationError(_('Height cannot be negative'))
            if record.weight and record.weight < 0:
                raise ValidationError(_('Weight cannot be negative'))
            if record.bmi and record.bmi < 0:
                raise ValidationError(_('BMI cannot be negative'))
