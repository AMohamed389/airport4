# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)

class employeetraining(models.Model):
    _name = 'employee.training'
    _description = 'Employee Trainings'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_training'
    _order = 'id DESC'

    trainee_type = fields.Selection([ ('Employee', 'Employee'),('External','External') ], string='Trainee Type' ,required=True,index=True)
    x_assign_date = fields.Date(string='Assign Date', index=True, tracking=True)

    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True, tracking=True, index=True )
    x_sector_name = fields.Char(string="Sector",related="x_employee_id.x_sector_name",store=True)
    x_public_administration_name = fields.Char(string="Public Administration" ,related="x_employee_id.x_public_administration_name",store=True)
    x_administration_name = fields.Char(string="Administration", related="x_employee_id.x_administration_name",store=True)
    x_section_name = fields.Char(string="Section",related="x_employee_id.x_section_name",store=True)
    
    supervisor_id = fields.Many2one('hr.employee', string="Supervisor", index=True )
    trainee_id = fields.Many2one('trainee', string='External Trainee',index=True)
    trainee_type_rel = fields.Selection( string='Trainee Source',related="trainee_id.trainee_type")

    x_staff_id = fields.Char(string='Staff Id', related="x_employee_id.x_staff_id")

    x_end_date = fields.Date(string='End Date', index=True, tracking=True,required=True)

    x_training = fields.Many2one('training.catalogue', string="Training", store=True, tracking=True, index=True ,required=True)
    
    x_training_type = fields.Selection(string="Training Type",related='x_training.x_training_type')

    x_training_code = fields.Char(string="Training Code", related='x_training.x_training_code')
    x_training_cost = fields.Monetary(string="Training Planned Cost", related='x_training.x_training_cost')
    x_training_actual_cost = fields.Monetary(string="Training Actual Cost",index=True,required=True)
    x_training_level = fields.Selection( string="Training Level",related="x_training.x_training_level")
    
    x_training_grade = fields.Selection(
        [('Fair', 'Fair'), ('Good', 'Good'), ('Very Good', 'Very Good'), ('Excellent', 'Excellent')],
        string="Training Grade", store=True, 
        index=True, tracking=True)

    x_notes = fields.Text(string="Notes", tracking=True, store=True)

    state = fields.Selection(
        [('New', 'New'), ('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'),('Completed','Completed') ,('Cancelled', 'Cancelled')],
        string="Status", store=True, 
        index=True, tracking=True, default='New')

    x_start_date = fields.Date(string='Start Date', index=True, tracking=True ,required=True)

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    training_budget_id = fields.Many2one('training_budget', string='Budget',copy=False)
    training_location_id = fields.Many2one('training_location', string='Training Location')
    trainer_id = fields.Many2one('trainer', string='Trainer')
    certificate = fields.Binary(string='Certificate')
    department_id = fields.Many2one('hr.department', string='Training Location Department')
    x_section_name_train_loc = fields.Char(index=True, string="Section (Training Location)", compute="_get_section_name", store=True)

    x_administration_name_train_loc = fields.Char(compute="_get_administration_name", index=True, string="Administration (Training Location)", store=True)

    x_public_administration_name_train_loc = fields.Char(compute="_get_public_administration_name", index=True, string="Public Administration (Training Location)", store=True)

    x_sector_name_train_loc = fields.Char(compute="_get_sector_name", index=True, string="Sector (Training Location)", store=True)
    qualitative_group_id = fields.Many2one('qualitative_group', string='Qualitative Group')

    @api.depends('department_id')
    def _get_section_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Department":
                _rec.x_section_name_train_loc = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Department":
                _rec.x_section_name_train_loc = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Department":
                _rec.x_section_name_train_loc = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Department":
                _rec.x_section_name_train_loc = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_section_name_train_loc = None
    
    @api.depends('department_id')
    def _get_administration_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Administration":
                _rec.x_administration_name_train_loc = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Administration":
                _rec.x_administration_name_train_loc = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Administration":
                _rec.x_administration_name_train_loc = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Administration":
                _rec.x_administration_name_train_loc = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_administration_name_train_loc = None
    
    @api.depends('department_id')
    def _get_public_administration_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Public Administration":
                _rec.x_public_administration_name_train_loc = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name_train_loc = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name_train_loc = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name_train_loc = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_public_administration_name_train_loc = None

    @api.depends('department_id')
    def _get_sector_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Sector":
                _rec.x_sector_name_train_loc = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Sector":
                _rec.x_sector_name_train_loc = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Sector":
                _rec.x_sector_name_train_loc = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Sector":
                _rec.x_sector_name_train_loc = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_sector_name_train_loc = None

    #def _get_employee_id(self):
        #_logger.info('Maged _get_employee_id default_x_employee_id ! ' + str(self._context.get('default_x_employee_id')))
        #if self._context.get('default_x_employee_id'):
            #return int(self._context.get('default_x_employee_id'))

    def default_get(self, fields):
        res = super(employeetraining, self).default_get(fields)

        try:
            if self._context and self._context is not None and self._context.get('default_x_employee_id'):
                res['x_employee_id'] = int(self._context.get('default_x_employee_id'))
                return res
        except:
            pass

        #res['x_notes'] = 'test'

        return res

    @api.onchange('x_training')
    def _onchange_x_training(self):
        if not self.x_training_actual_cost:
            self.x_training_actual_cost=self.x_training.x_training_cost
    
    def submit_training(self):
        domain=[('id', 'in', self.env.context.get('active_ids', [])),('state','=','New')]
        if not self.env.context.get('active_ids', []):
            domain=[('id', '=', self.id),('state','=','New')]
            
        trainings=self.env['employee.training'].search(domain)
        for r in trainings:

            recs = self.env['training_budget'].search([('start_date','<=',r.x_start_date),('end_date','>=',r.x_start_date)],limit=1)
            if not recs:
                    raise ValidationError(_("No Budget Assigned"))
            
            r.training_budget_id=recs.id
            r.state="Scheduled"

    def start_training(self):
        if self.state=="Scheduled":
            self.state="In Progress"

    def final_training(self):
        if not self.x_training_grade:
            raise ValidationError(_("Grade is mandatory"))
        if not self.certificate:
            raise ValidationError(_("Attach Certificate"))
        self.state="Completed"

    def cancel_training(self):
        #self.active=False
        self.state="Cancelled"

    @api.onchange('trainee_type')
    def _onchange_trainee_type(self):
        self.x_employee_id=False
        self.trainee_id =False

