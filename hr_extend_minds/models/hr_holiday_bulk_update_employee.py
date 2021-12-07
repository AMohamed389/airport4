# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date, timedelta
import calendar
from calendar import monthrange
from dateutil.relativedelta import *

import logging

_logger = logging.getLogger(__name__)


class hr_holiday_bulk_update_employee(models.Model):
    _name = 'hr_holiday_bulk_update_employee'
    _description = 'HR Holidays Bulk Update Employees'
    _order = 'id DESC'


    hr_holiday_bulk_update_id = fields.Many2one('hr_holiday_bulk_update', string="Batch Name", index=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", index=True)
    desc = fields.Text(string="Description", index=True)