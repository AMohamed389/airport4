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


class bonus_matrix(models.Model):
    _name = 'bonus_matrix'
    _description = 'Bonus Text'
    _order = 'id DESC'
    _rec_name = "periodic_bonus_percent"


    periodic_bonus_percent = fields.Float(string="Periodic Bonus %", index=True, tracking=True)
    basic_salary_periodic_bonus_date = fields.Date(string="Basic Salary Date", index=True, tracking=True)
    special_bonus_percent = fields.Float(string="Special Bonus %", index=True, tracking=True)
    special_bonus_folded = fields.Boolean(string="Special Bonus Is Folded ?", index=True, tracking=True)
    minimum = fields.Monetary(string="Minimum Periodic Bonus", index=True, tracking=True)
    maximum = fields.Monetary(string="Maximum Periodic Bonus", index=True, tracking=True)
    job_degree = fields.Selection([('الأولى','الأولى'),('الثانية','الثانية'),('الثالثة','الثالثة'),
    ('الرابعة','الرابعة'),('الخامسة','الخامسة'),('السادسة','السادسة'),
    ('عالية','عالية'),('ممتازة','ممتازة'),('مدير عام','مدير عام'),('عقد مؤقت','عقد مؤقت'),('أجر مقابل عمل','أجر مقابل عمل')] 
    ,string="Degree", index=True, required=True, tracking=True)
    exceptional_bonus_degrees = fields.Monetary(string="Exceptional Bonus", index=True, tracking=True)
    exceptional_bonus_folded = fields.Boolean(string="Exceptional Bonus Is Folded ?", index=True, tracking=True)
    previous_bonus = fields.Date(string="Previous Bonus Date", index=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)

    # _sql_constraints = [('constrain_cpmbine_1', 'UNIQUE (name, x_qualitative_group_id, x_order)', 'The combination qualitative group, job degree and order is already exists !.')]