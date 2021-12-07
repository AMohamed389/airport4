# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date
import mimetypes
import sys
import logging

_logger = logging.getLogger(__name__)


class training_location(models.Model):
    _name = 'training_location'
    _description = 'Training Location'
    _order = 'id DESC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Training Location", index=True, tracking=True)
    