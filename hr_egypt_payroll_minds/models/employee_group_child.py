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


class employee_group_child(models.Model):
    _name = 'employee_group_child'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Group Child'
    _order = 'id DESC'

    name = fields.Char(string="Name", index=True, tracking=True)
    employee_group_id = fields.Many2one('employee_group', tracking=True, index=True, required=True) 
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
    