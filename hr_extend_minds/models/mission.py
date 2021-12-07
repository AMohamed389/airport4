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


class mission (models.Model):
    _description = 'Mission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id DESC'
    _name = 'mission'
  
    
    name = fields.Many2one('hr.employee', string='Employee' ,index=True,required=True)
    type = fields.Selection([ ('Travel', 'Travel'), ('Mission', 'Mission'), ('Conference', 'Conference'), ('Review', 'Review'), ('Training', 'Training'), ('Inspection', 'Inspection'), ], string='Type',required=True)
    start_date = fields.Date(string='Start Date',index=True,required=True)
    end_date = fields.Date(string='End Date',index=True,required=True)
    decision_number = fields.Char(string='Decision Number',required=True)
    attachment = fields.Binary(string='Attachment')
    state = fields.Selection([ ('New', 'New'),('Submit','Submit') ], string='Status',default="New",index=True)
    desc = fields.Text(string='Description')
    destination_country = fields.Many2one('res.country', string='Destination Country')
    
    def submit(self):
        self.state="Submit"

    
    

    def name_get(self):
            result = []
            for rec in self:
                name =rec.name.name +' - '+self.type 
                result.append((rec.id, name))
            return result





    #_sql_constraints = [('constrainname', 'UNIQUE (name)', 'This mission already exists')]
    



    
  
  
