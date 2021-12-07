# -*- coding: utf-8 -*-

from re import T
from odoo import models, fields, api

from datetime import datetime
from datetime import date
from copy import deepcopy

import logging
_logger = logging.getLogger(__name__)


class taxation(models.Model):
    _inherit = 'hr.payslip.line'

    merit_id = fields.Many2one('allowance', string="Merit", index=True)
    deduction_id = fields.Many2one('deduction', string="Merit", index=True)
    subscription_id = fields.Many2one('subscription', string="Subscription", index=True)
    salary_rule_code = fields.Char(related='salary_rule_id.code', readonly=True, store=True)
    category_code = fields.Char(related='category_id.code', readonly=True, store=True)