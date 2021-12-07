# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)


class hrContractExtend(models.Model):

    _inherit = "hr.contract"

