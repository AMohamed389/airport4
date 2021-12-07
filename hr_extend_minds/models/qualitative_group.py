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


class qualitative_group(models.Model):
    _name = 'qualitative_group'
    _description = 'Qualitative Group'
    _order = 'id DESC'

    name = fields.Char(string="Qualitative Group", index=True, required=True, tracking=True)
    # x_job_position_id = fields.Many2one('hr.job', string="Job Position", index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)