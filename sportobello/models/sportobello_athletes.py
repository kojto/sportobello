from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
import re
import secrets
import string


class SportobelloAthlete(models.Model):
    _name = 'sportobello.athletes'
    _description = 'Sport Club Athletes'
    _rec_name = 'athlete_full_name'

    active = fields.Boolean(string='Active', default=True)
    identifier = fields.Char(string='ID Number')

    athlete_registry_number = fields.Char(string='Registry #')
    athlete_registry_date = fields.Date(string='Registry Date')
    athlete_registry_institution = fields.Char(string='Registry Institution')
    athlete_recent_medical_exam_date = fields.Date(string='Recent Medical Exam Date')

    athlete_first_name = fields.Char(string='First Name', required=True)
    athlete_middle_name = fields.Char(string='Middle Name')
    athlete_last_name = fields.Char(string='Last Name', required=True)
    athlete_full_name = fields.Char(string='Athlete', compute='compute_athlete_full_name', store=True)
    athlete_email = fields.Char(string='Email')
    athlete_phone = fields.Char(string='Phone')
    athlete_birth_date = fields.Date(string='Birth Date', required=True)
    athlete_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    athlete_nationality = fields.Char(string='Nationality', default='Bulgaria')
    athlete_zip_code = fields.Char(string='Zip Code', default="1000")

    athlete_address_line = fields.Char(string='Address')
    athlete_city = fields.Char(string='City', default="Sofia")
    athlete_country = fields.Char(string='Country', default='Bulgaria')
    athlete_county = fields.Char(string='County', default='Sofia')

    parent_first_name = fields.Char(string='Parent First Name')
    parent_middle_name = fields.Char(string='Parent Middle Name')
    parent_last_name = fields.Char(string='Parent Last Name')
    parent_email = fields.Char(string='Parent Email')
    parent_phone = fields.Char(string='Parent Phone')
    parent_relationship = fields.Selection([('mother', 'Mother'), ('father', 'Father'), ('guardian', 'Guardian')], string='Relationship to Athlete')

    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    emergency_contact_relationship = fields.Char(string='Emergency Contact Relationship')

    athlete_disease = fields.Text(string='Diseases', help='List of diseases or medical conditions')
    athlete_allergies = fields.Text(string='Allergies', help='List of allergies and reactions')

    anthropometric_tracker_ids = fields.One2many('sportobello.athlete.anthropometric.tracker', 'athlete_id', string='Anthropometric Data')
    overtraining_tracker_ids = fields.One2many('sportobello.athlete.overtraining.tracker', 'athlete_id', string='Overtraining Tracking')
    functional_test_tracker_ids = fields.One2many('sportobello.athlete.functional.test.tracker', 'athlete_id', string='Functional Testing')

    training_group_ids = fields.Many2many('sportobello.athlete.training.group', 'athlete_training_group_rel', 'athlete_id', 'training_group_id', string='Training Groups')

    associated_contact_id = fields.Many2one('kojto.contacts', string='Associated Contact', store=True)
    associated_user_id = fields.Many2one('res.users', string='Associated User', ondelete='set null')

    def open_related_contact(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kojto.contacts',
            'view_mode': 'form',
            'res_id': self.associated_contact_id.id,
            'target': 'new',
        }

    def create_related_contact(self):
        for athlete in self:
            if not athlete.identifier:
                raise ValidationError(_('Athlete must have an identification number'))

            existing_contact = self.env['kojto.contacts'].search([
                ('registration_number', '=', athlete.identifier)
            ], limit=1)

            if existing_contact:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'kojto.contacts',
                    'view_mode': 'form',
                    'res_id': existing_contact.id,
                    'target': 'new',
                }

            contact_data = {
                'registration_number': athlete.identifier,
                'name': athlete.athlete_full_name or f"{athlete.athlete_first_name} {athlete.athlete_last_name}",
                'contact_type': 'person',
                'active': True,
            }

            if athlete.athlete_phone:
                contact_data['phones'] = [(0, 0, {'name': athlete.athlete_phone})]

            new_contact = self.env['kojto.contacts'].create(contact_data)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'kojto.contacts',
                'view_mode': 'form',
                'res_id': new_contact.id,
                'target': 'new',
            }

    def add_system_user_to_athlete(self):
        for athlete in self:
            if not athlete.athlete_birth_date:
                raise ValidationError(_('Athlete must have a birth date to generate a system user'))

            if not athlete.athlete_first_name:
                raise ValidationError(_('Athlete must have a first name to generate a system user'))

            first_letter = athlete.athlete_first_name[0].lower() if athlete.athlete_first_name else ''

            dob_str = athlete.athlete_birth_date.strftime('%Y%m%d')

            email = f"{first_letter}{dob_str}@sportobello.com"

            existing_user = self.env['res.users'].search([('login', '=', email)], limit=1)

            athletes_group = self.env.ref('sportobello.group_sportobello_athletes', raise_if_not_found=False)

            if existing_user:
                if athletes_group and athletes_group not in existing_user.groups_id:
                    try:
                        self.env.cr.execute("""
                            INSERT INTO res_groups_users_rel (gid, uid)
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING
                        """, (athletes_group.id, existing_user.id))
                        existing_user.invalidate_recordset(['groups_id'])
                        athletes_group.invalidate_recordset(['users'])
                    except Exception:
                        pass
                athlete.write({'associated_user_id': existing_user.id})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('User Already Exists'),
                        'message': _('User with email %s already exists and has been linked to this athlete.') % email,
                        'type': 'info',
                        'sticky': False,
                    }
                }

            user_vals = {
                'name': athlete.athlete_full_name or f"{athlete.athlete_first_name} {athlete.athlete_last_name}",
                'login': email,
                'email': email,
            }

            new_user = self.env['res.users'].with_context(no_reset_password=True).create(user_vals)

            # Generate random password (12 characters: letters, digits, and special chars)
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            random_password = ''.join(secrets.choice(alphabet) for _ in range(12))
            new_user.password = random_password

            if athletes_group:
                new_user.flush_recordset()
                try:
                    self.env.cr.execute("""
                        INSERT INTO res_groups_users_rel (gid, uid)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (athletes_group.id, new_user.id))
                    new_user.invalidate_recordset(['groups_id'])
                    athletes_group.invalidate_recordset(['users'])
                except Exception:
                    pass

            athlete.write({'associated_user_id': new_user.id})

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('User Created Successfully'),
                    'message': _('System user created with email: %s and password: %s') % (email, random_password),
                    'type': 'success',
                    'sticky': False,
                }
            }

    @api.constrains('identifier')
    def restrict_duplicates(self):
        for rec in self:
            duplicates = self.env['sportobello.athletes'].search(
                [('identifier', '=', rec.identifier),
                 ('id', '!=', rec.id)])
            if duplicates:
                raise ValidationError(
                    _(f'Athlete with identifier: {rec.identifier} is already registered'))

    @api.onchange('athlete_first_name', 'athlete_middle_name', 'athlete_last_name', 'athlete_address_line')
    def check_forbidden_characters(self):
        forbidden_fields = {
            'athlete_first_name': self.athlete_first_name,
            'athlete_middle_name': self.athlete_middle_name,
            'athlete_last_name': self.athlete_last_name,
            'athlete_address_line': self.athlete_address_line,
        }

        for field, value in forbidden_fields.items():
            if re.search(r'[<>&]', value or ''):
                return {
                    'warning': {
                        'title': _("ERROR!"),
                        'message': _("Symbols <, >, and & are not allowed in field %s") % field,
                    }
                }

    @api.depends('athlete_first_name', 'athlete_middle_name', 'athlete_last_name')
    def compute_athlete_full_name(self):
        for record in self:
            if record.athlete_middle_name:
                full_name = f"{record.athlete_first_name} {record.athlete_middle_name} {record.athlete_last_name}"
            else:
                full_name = f"{record.athlete_first_name} {record.athlete_last_name}"

            record.athlete_full_name = full_name

    def create_kojto_contact_record(self):
        if not self:
            return

        contact_model = self.env['kojto.contacts']
        try:
            language_id = self.env.ref('base.lang_bg').id
        except ValueError:
            language_id = self.env.ref('base.lang_en').id

        created_contacts = self.env['kojto.contacts']
        success_count = 0
        error_count = 0
        total_count = len(self)

        for record in self:
            if not record.identifier or not record.athlete_full_name:
                raise ValidationError(f"Missing required fields (identifier or athlete_full_name) for record {record.id}")

            kojto_contact = contact_model.search([('registration_number', '=', record.identifier)], limit=1)

            valid_email = None
            if record.athlete_email and '@' in record.athlete_email and '.' in record.athlete_email.split('@')[-1]:
                valid_email = record.athlete_email

            contact_data = {
                'registration_number': record.identifier,
                'name': record.athlete_full_name,
                'contact_type': 'person',
                'is_non_EU': False,
                'active': True,
                'addresses': [(0, 0, {
                    'address': record.athlete_address_line or '',
                    'city': record.athlete_city or '',
                    'country_id': self.env.ref('base.bg').id,
                    'language_id': language_id,
                })],
                'emails': [(0, 0, {
                    'name': valid_email,
                })] if valid_email else [],
                'phones': [(0, 0, {
                    'name': record.athlete_phone or '',
                })] if record.athlete_phone else [],
            }

            try:
                if kojto_contact:
                    existing_addresses = kojto_contact.addresses
                    existing_emails = kojto_contact.emails
                    existing_phones = kojto_contact.phones

                    kojto_contact.write({
                        'registration_number': contact_data['registration_number'],
                        'name': contact_data['name'],
                        'contact_type': contact_data['contact_type'],
                        'is_non_EU': contact_data['is_non_EU'],
                        'active': contact_data['active'],
                    })

                    if existing_addresses:
                        existing_addresses[0].write(contact_data['addresses'][0][2])
                    else:
                        kojto_contact.write({'addresses': contact_data['addresses']})

                    if existing_emails and contact_data['emails']:
                        existing_emails[0].write(contact_data['emails'][0][2])
                    elif contact_data['emails']:
                        kojto_contact.write({'emails': contact_data['emails']})

                    if existing_phones and contact_data['phones']:
                        existing_phones[0].write(contact_data['phones'][0][2])
                    elif contact_data['phones']:
                        kojto_contact.write({'phones': contact_data['phones']})
                else:
                    kojto_contact = contact_model.create(contact_data)

                created_contacts |= kojto_contact
                success_count += 1

            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Failed to create/update contact for {record.athlete_full_name}: {str(e)}")
                error_count += 1
                continue

        if success_count > 0 or error_count > 0:
            message = f"Batch processing completed: {success_count} contacts created/updated successfully"
            if error_count > 0:
                message += f", {error_count} failed"
            message += f" out of {total_count} total records."

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Contact Creation Summary',
                    'message': message,
                    'type': 'success' if error_count == 0 else 'warning',
                    'sticky': True,
                }
            }

        return
