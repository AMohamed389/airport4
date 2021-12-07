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


class salary_degree(models.Model):
    _name = 'salary_degree'
    _description = 'Salary Degree'
    _order = 'id DESC'

    name = fields.Selection([('الأولى','الأولى'),('الثانية','الثانية'),('الثالثة','الثالثة'),
    ('الرابعة','الرابعة'),('الخامسة','الخامسة'),('السادسة','السادسة'),
    ('عالية','عالية'),('ممتازة','ممتازة'),('مدير عام','مدير عام'),('عقد مؤقت','عقد مؤقت'),('أجر مقابل عمل','أجر مقابل عمل')] 
    ,string="Degree", index=True, required=True, tracking=True)

    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)

    amount = fields.Monetary(string='Amount',index=True, required=True,tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)