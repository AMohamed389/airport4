# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date


import logging
_logger = logging.getLogger(__name__)


class myfn (models.AbstractModel):
    _name = 'myfn'
    _description = 'myfn'

    



