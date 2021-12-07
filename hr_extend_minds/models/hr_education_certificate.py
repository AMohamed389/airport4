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


class hr_education_cetificate(models.Model):
    _name = 'hr_education_certificate'
    _description = 'HR Employees Education Certificates'
    _order = 'x_certificate_date DESC'

    name = fields.Char(string="Name", index=True, tracking=True)
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True,
                                     tracking=True, index=True)
    x_university_name = fields.Char(string="University Name", index=True, tracking=True)
    x_specialization = fields.Char(string="Specialization", index=True, tracking=True)
    x_certificate_date = fields.Date(string="Certificate Date", index=True, tracking=True)
    x_decision_number = fields.Integer(string="Decision Number", index=True, tracking=True)
    x_decision_date = fields.Date(string="Decision Date", index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)