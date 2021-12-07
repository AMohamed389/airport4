# -*- coding: utf-8 -*-
from re import T
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


class salary_supervision_job(models.Model):
    _name = 'salary_supervision_job'
    _description = 'Salary Supervision Job'
    _order = 'id DESC'

    supervision_job_id = fields.Many2one('hr.job',string="Supervision Job", domain="[['x_is_supervision_job','=','True']]", index=True, tracking=True)

    name = fields.Char(related="supervision_job_id.name", string='Supervision Job Name', index=True, store=True)

    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)

    amount = fields.Monetary(string='Amount',index=True, required=True,tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)