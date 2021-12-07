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


class salary_marital(models.Model):
    _name = 'salary_marital'
    _description = 'Salary Marital'
    _order = 'id DESC'

    name = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced'),
        ('widow and dependent', 'Widow And Dependent'),
        ('married and dependent', 'Married And Dependent'),
        ('divorced and dependent', 'Divorced And Dependent')
    ], string='Marital Status', tracking=True, index=True, required=True)

    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)

    no_of_children = fields.Integer(string='Number Of Children', tracking=True, index=True)

    amount = fields.Monetary(string='Amount',index=True, required=True,tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)