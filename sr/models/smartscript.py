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

class smartscript (models.AbstractModel):
    _name = 'smartscript'

    ss_emp_name = fields.Char(string='Employee Name')
    ss_address= fields.Char(string='Address')
    ss_military_status = fields.Selection([('Postponed','Postponed'),('Completed','Completed'),('Exempted','Exempted')],string="Military Status")
    ss_military_start_date = fields.Date(string='Military Start Date')
    ss_military_end_date = fields.Date(string='Military End Date')
    ss_marital = fields.Selection([ ('single', 'Single'), ('married', 'Married'), ('cohabitant', 'Legal Cohabitant'), ('widower', 'Widower'), ('divorced', 'Divorced') ], string='Marital Status', default='single')
    ss_identity_issuer = fields.Char(string='Identity Issuer')
    

    i_ss_emp_name = fields.Boolean(compute='_compute_i_ss_emp_name', string='i_ss_emp_name')
    i_ss_address = fields.Boolean(compute='_compute_i_ss_address', string='i_ss_address')
    i_ss_military_status = fields.Boolean(compute='_compute_i_ss_military_status', string='i_ss_military_status')
    
    @api.depends('sub_category_id')
    def _compute_i_ss_emp_name(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_emp_name'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_emp_name=False
        else:
            self.i_ss_emp_name=True

    
        
    @api.depends('sub_category_id')
    def _compute_i_ss_address(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_address'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_address=False
        else:
            self.i_ss_address=True

    
        
    @api.depends('sub_category_id')
    def _compute_i_ss_military_status(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_military_status'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_military_status=False
        else:
            self.i_ss_military_status=True

    i_ss_military_start_date = fields.Boolean(compute='_compute_i_ss_military_start_date', string='i_ss_military_start_date')
        
    @api.depends('sub_category_id')
    def _compute_i_ss_military_start_date(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_military_start_date'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_military_start_date=False
        else:
            self.i_ss_military_start_date=True

    i_ss_military_end_date = fields.Boolean(compute='_compute_i_ss_military_end_date', string='i_ss_military_end_date')
        
    @api.depends('sub_category_id')
    def _compute_i_ss_military_end_date(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_military_end_date'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_military_end_date=False
        else:
            self.i_ss_military_end_date=True


    i_ss_marital = fields.Boolean(compute='_compute_i_ss_marital', string='i_ss_marital')
        
    @api.depends('sub_category_id')
    def _compute_i_ss_marital(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_marital'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_marital=False
        else:
            self.i_ss_marital=True
    

    i_ss_identity_issuer = fields.Boolean(compute='_compute_i_ss_identity_issuer', string='i_ss_identity_issuer')
        
    @api.depends('sub_category_id')
    def _compute_i_ss_identity_issuer(self):
        recs = self.env['sr_field'].search([('name.name','=','ss_identity_issuer'),('sub_category_id','=',self.sub_category_id.id)],limit=1)
        if(recs):
            self.i_ss_identity_issuer=False
        else:
            self.i_ss_identity_issuer=True


    





    



  
    