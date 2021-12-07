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


class trainingcatalogue(models.Model):
    _name = 'training.catalogue'
    _description = 'Training Catalogue'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_name'
    _order = 'create_date DESC'

    x_training_cost = fields.Monetary(string='Training Cost', index=True, tracking=True, store=True,
                                      currency_field='x_currency_id')

    x_image = fields.Binary(string='Image', store=True)

    x_name = fields.Char(string='Name', store=True, index=True, tracking=True ,required=True)

    x_training_type = fields.Selection(
        [('Technical', 'Technical'), ('Managerial', 'Managerial'), ('IT', 'IT'), ('Languages', 'Languages'),
         ('Diploma', 'Diploma'), ('Seminars And Conferences', 'Seminars And Conferences')],
        string="Training Type", store=True, 
        index=True, tracking=True)

    x_training_code = fields.Char(string='Training Code', store=True,required=True, index=True, tracking=True)

    x_training_level = fields.Selection(
        [('Basic', 'Basic'), ('Advanced', 'Advanced'), ('Specialist', 'Specialist'),('None','None')],
        string="Training Level", store=True, 
        index=True, tracking=True)

    x_notes = fields.Text(string="Notes", tracking=True, store=True)

    x_responsible_id = fields.Many2one('hr.employee', string="Responsible", store=True,
                                           tracking=True, index=True)

    x_currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)
    
    x_description = fields.Text(string='Description')

    trainee_ids = fields.One2many('employee.training', 'x_training', string='Trainees')

    budget_actual = fields.Monetary(compute='_compute_budget_actual', string='Actual Used')
    employee_count= fields.Integer(compute='_compute_budget_actual', string='Trainees Count')



    
    @api.depends('trainee_ids')
    def _compute_budget_actual(self):
        
        for r in self:
            recs = self.env['employee.training'].search([('x_training', "=", r.id),('state', "in", ['Scheduled','In Progress','Completed'])])
            r.budget_actual = sum(recs.mapped("x_training_actual_cost"))
            r.employee_count = len(recs.mapped("id"))

    _sql_constraints = [('constrainname', 'UNIQUE (x_training_code)', 'Training Code already exists!.')]