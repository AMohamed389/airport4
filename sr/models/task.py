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

class task (models.Model):
    _name = 'task'

    name = fields.Char(string='Name', index=True, required=True)
    sub_category_id = fields.Many2one( 'sub_category', string='Sub Category', index=True, required=True)
    res_group_id = fields.Many2one( 'res.groups', string='group', index=True, required=True)
    desc = fields.Text(string='Description')
    seq = fields.Integer(string='Sequence')
    next_seq = fields.Integer(string='Next Sequence')
    action_id = fields.Many2one('action', string='action')
    #code = fields.Text(string='code',related="action_id.code")

    
    
            


            

    _sql_constraints = [ ('constrainname', 'UNIQUE (seq,name,sub_category_id)', 'This task already exists')]
