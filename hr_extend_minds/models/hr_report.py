# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class hr_report(models.Model):
    _name = 'hr_report'
    _description = 'HR Reports'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id DESC'

    name = fields.Selection([('Statement Letter','Statement Letter'),('HR Letter','HR Letter')], string="Document", index=True, required=True, tracking=True)
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True, required=True, tracking=True, index=True)
    state = fields.Selection([
        ('Draft', 'Draft'),('Submit', 'Submit'),('Completed', 'Completed')
    ], string='Report State' ,default='Draft', index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True)



    def submit_report(self):
        for _rec in self:
            _rec.state = 'Submit'
    
    def print_document(self):
        for _rec in self:

            #_view_name = ""
            _context = ""
            _res_model = ""
            _target = "new"
            _name = ""

            if _rec.name == "Statement Letter":
                _name = "Statement Letter"
                _res_model = 'hr_statement_document'
                _context = {
                    'default_x_employee_id': _rec.x_employee_id.id,
                    'default_x_hr_report_id': _rec.id,
                }
            
            elif _rec.name == "HR Letter":
                _name = "HR Letter"
                _res_model = 'hr_letter_document'
                _context = {
                    'default_x_employee_id': _rec.x_employee_id.id,
                    'default_x_hr_report_id': _rec.id,
                }

            else:
                return False
            
            return {
                'name': _name,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': _res_model,
                'type': 'ir.actions.act_window',
                'target': _target,
                'res_id': False,
                'context': _context,
            }
            



    
