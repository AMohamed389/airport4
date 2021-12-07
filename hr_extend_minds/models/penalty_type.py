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


class penaltytype(models.Model):
    _name = 'penalty.type'
    _description = 'Penalty Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_name'
    _order = 'id DESC'

    # x_name = fields.Selection([('Warning','Warning'),
    #                             ('Salary Deduction','Salary Deduction'),
    #                             ('Postpone Entitlement Date Of Annual Allowance','Postpone Entitlement Date Of Annual Allowance'),
    #                             ('Deprivation Of A portion of The Annual Allowance','Deprivation Of A portion of The Annual Allowance'),
    #                             ('Postponse Promotion','Postponse Promotion'),
    #                             ('Reduce Salary','Reduce Salary'),
    #                             ('Reduce Position Or Reduce Degree','Reduce Position Or Reduce Degree'),
    #                             ('Severance','Severance'),
    #                             ('Absence Without Permission','Absence Without Permission'),
    #                             ('Attention','Attention'),
    #                             ('Deduction For Not Attending The Investigation','Deduction For Not Attending The Investigation'),
    #                           ], string='Name', store=True, index=True, tracking=True)

    x_name = fields.Char(string='Name', store=True, index=True, tracking=True)

    x_code = fields.Char(string='Penalty Code', store=True, index=True, tracking=True)

    x_notes = fields.Text(string="Notes", tracking=True, store=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)