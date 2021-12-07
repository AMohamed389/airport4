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


class job_degree(models.Model):
    _name = 'job_degree'
    _description = 'Job Degree'
    _order = 'id DESC'

    name = fields.Selection([('الأولى','الأولى'),('الثانية','الثانية'),('الثالثة','الثالثة'),
    ('الرابعة','الرابعة'),('الخامسة','الخامسة'),('السادسة','السادسة'),
    ('عالية','عالية'),('ممتازة','ممتازة'),('مدير عام','مدير عام'),('عقد مؤقت','عقد مؤقت'),('أجر مقابل عمل','أجر مقابل عمل')] 
    ,string="Degree", index=True, required=True, tracking=True)
    
    x_qualitative_group_id = fields.Many2one('qualitative_group', string="Qualitative Group", index=True, tracking=True)

    x_order = fields.Integer(string="Order", index=True, tracking=True)

    #x_job_id = fields.Many2one('hr.job', string="Job Position", index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)




    # _sql_constraints = [('constrain_cpmbine_1', 'UNIQUE (name, x_qualitative_group_id, x_order)', 'The combination qualitative group, job degree and order is already exists !.')]