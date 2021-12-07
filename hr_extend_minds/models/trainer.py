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

class trainer (models.Model):
    _description = 'Trainer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id DESC'
    _name = 'trainer'
  
    name = fields.Char(string='Trainer', index=True, required=True, copy=False)
    trainer_type = fields.Selection([ ('Employee', 'Employee'),('External','External') ], string='Trainer Type')
    employee_id = fields.Many2one('hr.employee', string='Employee', copy=False)
    mobile_phone = fields.Char(string='Mobile Number', copy=False)
    identification_id = fields.Char(string='Identification No', copy=False)
    trainer_code = fields.Char(string='Trainer Code', copy=False)
    active = fields.Boolean(string='Active',index=True,default=True)
    
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

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.name=self.employee_id.name
        self.mobile_phone=self.employee_id.mobile_phone
        self.identification_id=self.employee_id.identification_id
        self.trainer_code=self.employee_id.x_staff_id

    @api.onchange('trainer_type')
    def _onchange_trainer_type(self):
        self.employee_id =False
        self.name = False
        self.mobile_phone=False
        self.identification_id=False
        self.trainer_code=False

    

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        
        if name:
            domain = ['|','|', ('name', operator, name), ('identification_id', operator, name), ('trainer_code', operator, name)]
        

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)


    _sql_constraints = [('constrainname', 'UNIQUE (identification_id)', 'This identification id already exists')]
    
