# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class employee_card(models.Model):
    _name = 'employee_card'
    _description = 'Employee Card'
    _order = 'id DESC'
    _rec_name = "employee_name"

    employee_id = fields.Many2one('hr.employee', string="Employee", index=True, tracking=True)
    employee_name = fields.Char(related='employee_id.name', string="Employee Name", store=True, index=True, tracking=True)
    employee_staff_id = fields.Char(related='employee_id.x_staff_id', string="Employee Staff Id", store=True, index=True, tracking=True)
    employee_degree_id = fields.Many2one(related='employee_id.x_job_degree_id', string="Employee Degree Id", store=True, index=True, tracking=True)
    employee_job_id = fields.Many2one(related='employee_id.job_id', string="Employee Job Id", store=True, index=True, tracking=True)
    #qualitative_group_id = fields.Many2one('qualitative_group',string="Qualitative Group", index=True, tracking=True)
    job_degree_id = fields.Many2one('job_degree', string="Degree", domain=lambda self: "[['id','=', employee_degree_id]]", index=True, tracking=True)
    date = fields.Date(string='Date', index=True, tracking=True)
    job_id = fields.Many2one('hr.job', 'Job Position', domain=lambda self: "[['id','=', employee_job_id]]", index=True, tracking=True)
    basic_salary = fields.Monetary(string="Basic Salary", index=True, tracking=True)
    decision_number = fields.Integer(string='Decision Number', store=True, index=True, tracking=True)
    decision_date = fields.Date(string='Decision Date', index=True, tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)

    _sql_constraints = [('constrain_employee_id_date_active', 'UNIQUE (employee_id, date, active)', 'The combination employee, date and active is already exists !.')]