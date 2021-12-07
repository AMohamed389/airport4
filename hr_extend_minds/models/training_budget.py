# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date
import mimetypes
import sys
import logging

_logger = logging.getLogger(__name__)


class training_budget(models.Model):
    _name = 'training_budget'
    _description = 'Budget'
    _order = 'id DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Budget Name", index=True, tracking=True)
    start_date = fields.Date(string='Start Date',required=True,index=True,tracking=True)
    end_date = fields.Date(string='End Date',required=True,index=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    budget_planned = fields.Monetary(string='Planned Budget')
    budget_actual = fields.Monetary(compute='_compute_budget_actual', string='Actual Used')
    employee_count= fields.Integer(compute='_compute_budget_actual', string='Training Counts')
    budget_diff= fields.Monetary(compute='_compute_budget_actual', string='Available Budget')
    empolyee_ids = fields.One2many('employee.training', 'training_budget_id', string='employee training')

    @api.depends('budget_planned')
    def _compute_budget_actual(self):
        
        for r in self:
            recs = self.env['employee.training'].search([('training_budget_id', "=", r.id),('state', "in", ['Scheduled','In Progress','Completed'])])
        
            r.budget_actual = sum(recs.mapped("x_training_actual_cost"))
            r.employee_count = len(recs.mapped("id"))
            r.budget_diff = r.budget_planned - r.budget_actual