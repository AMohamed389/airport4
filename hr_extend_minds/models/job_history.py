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


class job_history(models.Model):
    _name = 'job_history'
    _description = 'Job History'
    _order = 'x_date_from DESC'

    name = fields.Char(string="Job", index=True, tracking=True)
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True,
                                     tracking=True, index=True)
    x_type = fields.Char(string="Type", index=True, tracking=True)
    x_source_company = fields.Char(string="Source Company", index=True, tracking=True)
    x_sector = fields.Char(string="Sector", index=True, tracking=True)
    x_public_administration = fields.Char(string="Public Administration", index=True, tracking=True)
    x_administration = fields.Char(string="Administration", index=True, tracking=True)
    x_department = fields.Char(string="Department", index=True, tracking=True)
    x_qualitative_group = fields.Char(string="Qualitative Group", index=True, tracking=True)
    x_degree = fields.Char(string="Degree", index=True, tracking=True)
    x_date_from = fields.Date(string="Date From", index=True, tracking=True)
    x_date_to = fields.Date(string="Date To", index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)