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


class hr_department(models.Model):
    _inherit = 'hr.department'

    x_type = fields.Selection([('Department','Department'),('Administration','Administration'),
    ('Public Administration','Public Administration'),('Sector','Sector')], string="Type", index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)