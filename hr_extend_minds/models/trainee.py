# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests

import logging
_logger = logging.getLogger(__name__)


class trainee (models.Model):
    _description = 'Trainee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id DESC'
    _name = 'trainee'

    trainee_type = fields.Selection(
        [('Undergraduate', 'Undergraduate'), ('External Company', 'External Company')], string='Trainee Type', required=True,)
    name = fields.Char(string='Trainee Name', index=True, required=True, copy=False)

    mobile_phone = fields.Char(string='Mobile Number', copy=False)
    identification_id = fields.Char(string='Identification No', copy=False ,required=True)
    trainer_code = fields.Char(string='Trainee Code', copy=False)
    university = fields.Char(string='University', index=True)
    active = fields.Boolean(string='Active', index=True, default=True)
    employee_training_id = fields.One2many('employee.training', 'trainee_id', string='Trainings')


    @api.constrains('mobile_phone')
    def _check_mobile_11(self):
        for rec in self:
            if len(str(rec.mobile_phone)) != 11:
                raise ValidationError("Mobile number should be 11 digits !.")


    @api.constrains('identification_id')
    def _check_id_number_14(self):
        for rec in self:
            if len(str(rec.identification_id)) != 14:
                raise ValidationError("National Id number should be 14 digits !.")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []

        if name:
            domain = ['|', '|', ('name', operator, name), ('identification_id',
                                                           operator, name), ('trainer_code', operator, name)]

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    _sql_constraints = [('constrainname', 'UNIQUE (identification_id)',
                         'This identification id already exists')]

    @api.onchange('trainee_type')
    def _onchange_trainee_type(self):
        self.university=False
