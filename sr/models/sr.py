# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr
import json
import datetime
import string
import requests
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class sr (models.Model):
    _name = 'sr'
    _inherit =['smartscript']
  
    name = fields.Char(string='SR Number' ,index=True, required=True,default="New")
    employee_id = fields.Many2one('hr.employee', string='Employee' ,required=True)
    category_id = fields.Many2one('category', string='Category',required=True)
    sub_category_id = fields.Many2one('sub_category', string='Sub Category',required=True)
    state = fields.Selection([ ('New', 'New'),('In Progress', 'In Progress'),('Done', 'Done'),('Cancelled', 'Cancelled'),('Rejected', 'Rejected') ], string='Status' , index=True,tracking=True,default="New") 
    current_seq = fields.Integer(string='Current seq',index=True,tracking=True)
    sr_task_ids = fields.One2many('sr_task', 'sr_id', string='Tasks')
    #smartscript_ids = fields.One2many('smartscript', 'sr_id', string='SmartScript')
    reason = fields.Text("Reason")


    
    

    def create_smartscript(self):
        for rec in self :


            pass

    def initiate_request(self):
        for rec in self:
            rec.state = "In Progress"
            rec.create_next_tasks()
            

    def create_next_tasks(self):
        self.check_if_inprogress()
        tasks = self.env['task'].search([('sub_category_id','=',self.sub_category_id.id),('seq','=',int(self.current_seq))])
        for t in tasks:
            newt=self.sr_task_ids.create({
                # 'name':t.name,
                'sr_id':self.id,
                'task_id':t.id,
                'current_seq':self.current_seq

                # 'res_group_id':t.res_group_id.id

            })
            newt.onchange_task_id()

        self.current_seq = t.next_seq
    
    def check_if_inprogress(self,raiseerror=True):
        if self.state != "In Progress":
            if raiseerror:
                raise ValidationError("SR not in 'In Progress' state")
            else:
                return False
        else:
            return True



    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('service_request_sequence')
        result = super(sr, self).create(vals)       
        return result


    def approve_request(self,task_id=False):
        for rec in self:
            rec.check_if_inprogress()
            if task_id:
                active_tasks = rec.sr_task_ids.search([("sr_id","=",rec.id),('state','=','In Progress'),('id','=',task_id)])
            else:
                active_tasks = rec.sr_task_ids.search([("sr_id","=",rec.id),('state','=','In Progress')])
            if not active_tasks:
                raise ValidationError("No Pending Tasks to Approve!")
            if(len(active_tasks) ==1):
                rec._approve(active_tasks)
            else:
                raise ValidationError("more than one Task")
        

    def _settel_all_activity(self):
        active_tasks = self.sr_task_ids.search([("sr_id","=",self.id),('state','=','In Progress')])
        for t in active_tasks:
            t.state = "Action by other"
            t.action_by  = self.env.user.id
            t.action_date =fields.datetime.now()




            
    def _approve(self,t):
        
        if not t.has_access :
            raise ValidationError("you are not authorized to approve this Task \r\n '%s' only could approve this request "%t.res_group_id )
        eval_context ={"self":self,"empid":self.employee_id.id }

        eval_context["ss_emp_name"]=self.ss_emp_name
        eval_context["ss_address"]=self.ss_address
        eval_context["ss_military_status"]=self.ss_military_status
        eval_context["ss_military_start_date"]=self.ss_military_start_date
        eval_context["ss_military_end_date"]=self.ss_military_end_date
        eval_context["ss_marital"]=self.ss_marital
        eval_context["ss_identity_issuer"]=self.ss_identity_issuer
        
        
            



        safe_eval(t.action_id.code.strip(), eval_context, mode="exec", nocopy=True)  # nocopy allows to return 'action'
        eCode = eval_context.get('eCode')
        eDesc = eval_context.get('eDesc')
        nextAction =eval_context.get('nextAction')
        
        t.action_by  = self.env.user.id
        t.action_date =fields.datetime.now()
        t.state="Done"

        if(nextAction.lower()=="r"):
            self.state="Rejected"
            self.reason = eDesc
            self._settel_all_activity()
            return
        elif(nextAction.lower() == "d"):
            self.state="Done"
            self.reason = eDesc
            self._settel_all_activity()
            return
        
        active_tasks = self.sr_task_ids.search([("sr_id","=",self.id),('state','=','In Progress'),('current_seq','=',t.current_seq)])
        
        if(self.current_seq==0):
            
            if not active_tasks:
                self.state="Done"
                return
        if not active_tasks:
            self.create_next_tasks()


        
    # def fields_view_get(self, view_id=None, view_type='form',toolbar=False, submenu=False):
    #     result = super(sr, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
    #     if view_type == 'form':
    #         doc = etree.XML(result['arch'])
    #         #   raise ValidationError(str(doc))
    #         f = doc.xpath("//field[@name='current_seq']")
    #         #raise ValidationError(f[0].get("string"))
    #         f[0].set("string", "test")
    #         #raise ValidationError(f[0])
    #         for fieldname in self.sub_category_id.sr_field_ids:
                
    #             f = doc.xpath("//field[@name="+'current_seq'+"]")
    #             if f:
    #                 f[0].set("string", fieldname.string_val)
    #             #sale_reference[0].addnext(etree.Element('label', {'string': 'Sale Reference Number'}))
    #         result['arch'] = etree.tostring(doc, encoding='unicode')
        
    #     return result

        


    
        
        

        



        #raise ValidationError(str(eCode) + "---" +str(eDesc))
        
        

        

        





    def reject_request(self,task_id=False):
        for rec in self:
            rec.check_if_inprogress()
            if task_id:
                active_tasks = rec.sr_task_ids.search([("sr_id","=",rec.id),('state','=','In Progress'),('id','=',task_id)])
            else:
                active_tasks = rec.sr_task_ids.search([("sr_id","=",rec.id),('state','=','In Progress')])
            if not active_tasks:
                raise ValidationError("No Pending Tasks to Approve!")
            if(len(active_tasks) ==1):
                rec._reject(active_tasks)
            else:
                raise ValidationError("more than one Task")

    def _reject(self,t):
        if not t.has_access :
            raise ValidationError("you are not authorized to approve this Task \r\n '%s' only could approve this request "%t.res_group_id )
        
        t.action_by  = self.env.user.id
        t.action_date =fields.datetime.now()

        t.state="Rejected"
        self.state="Rejected"
        self._settel_all_activity()
        
    
    