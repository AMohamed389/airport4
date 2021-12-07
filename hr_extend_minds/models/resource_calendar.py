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


class resource_calendar(models.Model):
    _inherit = 'resource.calendar'

    x_work_schedule_type = fields.Selection([('Morning','Morning'),
                ('Shift','Shift')], string='Work Schedule Type', index=True, tracking=True)