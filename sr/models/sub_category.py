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


class sub_category (models.Model):
    _name = 'sub_category'
  
    
    name = fields.Char(string='Sub Category' ,index=True, required=True)
    category_id = fields.Many2one('category', string='Category',index=True, required=True)
    task_ids = fields.One2many('task', 'sub_category_id', string='Child Task')
    sr_field_ids = fields.One2many('sr_field', 'sub_category_id', string='Fields')



    def name_get(self):
        result = []
        for rec in self:
            name =rec.category_id.name +" / "+  rec.name
            result.append((rec.id, name))
        return result

    
  
    





    _sql_constraints = [('constrainname', 'UNIQUE (name,category_id)', 'This sub_category already exists')]
    



    
  
  
