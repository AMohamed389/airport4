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


class hr_job(models.Model):
    _inherit = 'hr.job'
    _order = 'x_sector_name ASC, x_qualitative_group_name ASC,x_job_degree_order DESC'

    x_qualitative_group_id = fields.Many2one('qualitative_group',string="Qualitative Group", index=True, tracking=True)
    x_job_degree_id = fields.Many2one('job_degree', string="Degree", index=True, tracking=True)
    x_job_degree_order = fields.Integer(related='x_job_degree_id.x_order', string="Order", store=True, index=True, tracking=True)
    x_is_limited = fields.Boolean(string="Is Limited ?", index=True, tracking=True)
    x_job_responsibilities = fields.Text(string="Responsibilities", tracking=True)
    x_job_qualifications = fields.Text(string="Qualifications", tracking=True)
    x_sector_id = fields.Many2one('hr.department', domain=[['x_type','=','Sector']], string="Sector", index=True, tracking=True)
    x_sector_name = fields.Char(related='x_sector_id.name', string="Sector", store=True, index=True, tracking=True)
    x_qualitative_group_name = fields.Char(related='x_qualitative_group_id.name', string="Qualitative Group", store=True, index=True, tracking=True)
    x_is_supervision_job = fields.Boolean(string="Is Supervision Job ?", index=True, tracking=True)
    allowance_id = fields.Many2one(string="Allowance", domain=[('Type','=','Allowance')], index=True, tracking=True)

    hr_employee_id = fields.Many2one('hr.employee')

    