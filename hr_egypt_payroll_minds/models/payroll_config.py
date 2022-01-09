# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class payroll_config(models.Model):
    _name = 'payroll_config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Payroll Configuration'
    _order = 'id DESC'

    name = fields.Char(string="Key", index=True, tracking=True)
    # val = fields.Char(string="Value", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
    

    def activate_dynamic(self):
        for _rec in self:
            _rec.sudo().active = True

    def deactivate_dynamic(self):
        for _rec in self:
            _rec.sudo().active = False