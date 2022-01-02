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


class sr_task (models.Model):
    _name = 'sr_task'
  
    
    name = fields.Char(string='Name' ,index=True)
    sr_id = fields.Many2one('sr', string='Service Request',index=True)
    task_id = fields.Many2one('task', string='Task')
    res_group_id = fields.Many2one( 'res.groups', string='Group', index=True)

    has_access = fields.Boolean(compute='_compute_has_access', string='Has access')
    state = fields.Selection([ ('In Progress', 'In Progress'),('Done','Done'),('Rejected','Rejected'),('Cancelled','Cancelled'),('Action by other','Action by other') ], string='Status' ,default="In Progress")
    action_by = fields.Many2one('res.users', string='Action by')
    action_date = fields.Datetime(string='Action Date')
    action_id = fields.Many2one('action',string='code',related="task_id.action_id")
    current_seq = fields.Integer(string='Current seq',index=True,tracking=True)
    
    
    
    @api.depends('has_access')
    def _compute_has_access(self):
        for rec in self :
            if not rec.res_group_id:
                rec.has_access = False 
                return
            xmlid= self.env['ir.model.data'].search([('res_id','=',rec.res_group_id.id),('model','=','res.groups')],limit=1)
            #raise ValidationError(rec.res_group_id.full_name + " ---" +xmlid.complete_name)
            if self.env.user.has_group(xmlid.complete_name ):
                rec.has_access = True
            else:
                rec.has_access = False


    @api.onchange('task_id')
    def onchange_task_id(self):
        for rec in self:
            rec.res_group_id = rec.task_id.res_group_id
            rec.name = rec.task_id.name

    # def has_group(self ,group_id):
    #     uid =self.env.user.id
    #     u = self.env['res.users'].search([('id','=',uid)],limit=1)
    #     if not u or not group_id:
    #         return False
    #     gf=u.groups_id.search([('gid','=',group_id)],limit=1)
    #     if gf:
    #         return True
    #     return False


    def approve_request(self):
        for rec in self:
            rec.sr_id.approve_request(rec.id)
    
    def reject_request(self):
        for rec in self:
            rec.sr_id.reject_request(rec.id)
        

        

        

    
    

    
  
    





    
    



    
  
  
