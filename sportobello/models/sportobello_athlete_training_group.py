# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SportobelloAthleteTrainingGroup(models.Model):
    _name = 'sportobello.athlete.training.group'
    _description = 'Training Group'
    _rec_name = 'name'

    name = fields.Char(string='Group Name', required=True)
    athlete_ids = fields.Many2many('sportobello.athletes', 'athlete_training_group_rel', 'training_group_id', 'athlete_id', string='Athletes')
