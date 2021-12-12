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


class incentive_band(models.Model):
    _name = 'incentive_band'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Incentive Band'
    _order = 'id DESC'

    name = fields.Char(string="Name", index=True, tracking=True)  
    code = fields.Char(string="Code", index=True, tracking=True)  
    desc = fields.Char(string="Description", index=True, tracking=True)  
    type = fields.Selection([('حافز وظيفي','حافز وظيفي'),('حافز اضافي','حافز اضافي')], string="Type", index=True, tracking=True)  
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
    