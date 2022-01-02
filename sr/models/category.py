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


class category (models.Model):
    _name = 'category'
  
    
    name = fields.Char(string='Name' ,index=True, required=True)
    
    

    
  
    





    _sql_constraints = [('constrainname', 'UNIQUE (name)', 'This Category already exists')]
    



    
  
  
