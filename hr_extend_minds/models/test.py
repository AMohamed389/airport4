# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests

import logging
_logger = logging.getLogger(__name__)

class test_image (models.Model):
    _description = 'test_image'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id DESC'
    _name = 'test_image'

    name = fields.Char()
    att = fields.Binary()
    employee_id = fields.Many2one('hr.employee')
  