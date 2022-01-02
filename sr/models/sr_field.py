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


class sr_field (models.Model):
    _name = 'sr_field'
  
    
    name = fields.Many2one('ir.model.fields',domain=[['model_id','=','smartscript'],['name', 'like', 'ss_%'],['store', '=', True]], string='Field')
    string_val = fields.Char(string='String')
    model_id = fields.Many2one('ir.model', string='Model')
    ttype = fields.Selection( related="name.ttype", string='Field type')
    sub_category_id = fields.Many2one( 'sub_category', string='Sub Category', index=True, required=True)
    active = fields.Boolean(string='Active',default=True)
    
    
    

    
  
    





    _sql_constraints = [('constrainname', 'UNIQUE (name,sub_category_id)', 'This Field already exists')]
    



    
  
  
