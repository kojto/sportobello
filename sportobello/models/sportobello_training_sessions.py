# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SportobelloTrainingSessions(models.Model):
    _name = 'sportobello.training.sessions'
    _description = 'Training Sessions'
    _rec_name = 'name'
    _order = 'name desc'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    session_of_day = fields.Selection([('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th'), ('5', '5th')], string='Session', required=True, default='1')

    training_session_line_ids = fields.One2many('sportobello.training.session.lines', 'calendar_id', string='Elements')

    training_session_text_only = fields.Text(string='Training Session', compute='_compute_training_session_text_only')

    training_session_completed_by = fields.Many2many('sportobello.athletes', relation='sportobello_training_session_completed_by_rel', string='Completed by')
    training_session_intended_for = fields.Many2many('sportobello.athletes', relation='sportobello_training_calendar_for_rel', string='Training for')
    training_group_ids = fields.Many2many('sportobello.athlete.training.group', relation='sportobello_training_calendar_groups_rel', string='Add athletes from groups')

    @api.onchange('training_group_ids')
    def _onchange_training_group_ids(self):
        if self.training_group_ids:
            athlete_ids = []
            for group in self.training_group_ids:
                athlete_ids.extend(group.athlete_ids.ids)
            self.training_session_intended_for = [(6, 0, list(set(athlete_ids)))]
            self.training_session_completed_by = [(6, 0, list(set(athlete_ids)))]

    def action_clear_training_group_ids(self):
        for record in self:
            record.training_group_ids = [(5, 0, 0)]
        return True

    def action_clear_training_session_intended_for(self):
        for record in self:
            record.training_session_intended_for = [(5, 0, 0)]
        return True

    def action_clear_training_session_completed_by(self):
        for record in self:
            record.training_session_completed_by = [(5, 0, 0)]
        return True

    def action_insert_all_training_groups(self):
        for record in self:
            all_groups = self.env['sportobello.athlete.training.group'].search([])
            existing_group_ids = record.training_group_ids.ids
            new_group_ids = [g.id for g in all_groups if g.id not in existing_group_ids]
            if new_group_ids:
                record.training_group_ids = [(4, gid) for gid in new_group_ids]
        return True

    def action_insert_all_athletes_for(self):
        for record in self:
            all_athletes = self.env['sportobello.athletes'].search([('active', '=', True)])
            existing_athlete_ids = record.training_session_intended_for.ids
            new_athlete_ids = [a.id for a in all_athletes if a.id not in existing_athlete_ids]
            if new_athlete_ids:
                record.training_session_intended_for = [(4, aid) for aid in new_athlete_ids]
        return True

    def action_insert_all_athletes_completed_by(self):
        for record in self:
            all_athletes = self.env['sportobello.athletes'].search([('active', '=', True)])
            existing_athlete_ids = record.training_session_completed_by.ids
            new_athlete_ids = [a.id for a in all_athletes if a.id not in existing_athlete_ids]
            if new_athlete_ids:
                record.training_session_completed_by = [(4, aid) for aid in new_athlete_ids]
        return True

    @api.depends('date', 'session_of_day')
    def _compute_name(self):
        for record in self:
            if record.date and record.session_of_day:
                date_str = record.date.strftime('%Y-%m-%d')
                session_label = dict(record._fields['session_of_day'].selection).get(record.session_of_day, record.session_of_day)

                session_label = session_label.replace(' Session', '')
                record.name = f"{date_str}_{session_label}"
            else:
                record.name = 'Training Session'

    @api.depends('training_session_line_ids.training_session_id.name', 'training_session_line_ids.training_session_id.description')
    def _compute_training_session_text_only(self):
        for record in self:
            training_sessions = record.training_session_line_ids.mapped('training_session_id')
            if training_sessions:
                numbered_lines = []
                for index, session in enumerate(training_sessions, start=1):
                    name = session.name or ''
                    description = session.description or ''
                    numbered_lines.append(f"{index}. {name}: {description}")
                record.training_session_text_only = '\n'.join(numbered_lines)
            else:
                record.training_session_text_only = False
