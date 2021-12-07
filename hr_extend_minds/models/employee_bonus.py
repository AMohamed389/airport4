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


class employee_bonus(models.Model):
    _name = 'employee_bonus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Bonus'
    _order = 'id DESC'
    _rec_name = "employee_name"
    
    employee_id = fields.Many2one('hr.employee', string="Employee", index=True, tracking=True)
    batch_id = fields.Many2one('bonus_batch', string="Batch", index=True, tracking=True)
    batch_state = fields.Selection(related='batch_id.state', string="Batch Status", index=True, tracking=True)
    employee_name = fields.Char(related='employee_id.name', string="Employee Name", index=True, tracking=True)
    employee_staff_id = fields.Char(related='employee_id.x_staff_id', string="Employee Staff Id", index=True, tracking=True)
    qualitative_group_id = fields.Many2one('qualitative_group',string="Qualitative Group", index=True, tracking=True)
    current_basic_salary = fields.Monetary(string="Current Basic Salary", index=True, tracking=True)
    periodic_bonus = fields.Monetary(string="Periodic Bonus", index=True, tracking=True)
    special_bonus = fields.Monetary(string="Special Bonus", index=True, tracking=True)
    previous_bonus = fields.Monetary(string="Previous Bonus", index=True, tracking=True)
    exceptional_bonus = fields.Monetary(string="Exceptional Bonus", index=True, tracking=True)
    new_basic_salary = fields.Monetary(string="New Basic Salary", index=True, tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)

    # _sql_constraints = [('constrain_cpmbine_1', 'UNIQUE (name, x_qualitative_group_id, x_order)', 'The combination qualitative group, job degree and order is already exists !.')]