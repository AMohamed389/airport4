# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class bonus_batch(models.Model):
    _name = 'bonus_batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bonus Batch'
    _order = 'id DESC'

    name = fields.Char(string="Name", index=True, tracking=True)
    date = fields.Date(string='Date', index=True, tracking=True)
    number_of_employees = fields.Integer(string="No. Of Employees", compute="_get_number_of_employees")
    employee_bonus = fields.One2many('employee_bonus', 'batch_id', string="Employees")
    state = fields.Selection(
        [('Draft', 'Draft'), ('In Review', 'In Review'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        string="Status", store=True, 
        index=True, tracking=True, default='Draft')    

    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)

    _sql_constraints = [('constrain_date_state_name', 'UNIQUE (date,state,name)', 'The batch name, date and state is already exists !.')]


    def _get_number_of_employees(self):
        for _rec in self:
            _rec.number_of_employees = len(_rec.employee_bonus) #.search_count([])
            return _rec.number_of_employees
        return 0

    def cancel(self):
        for _rec in self:
            for __rec in _rec.employee_bonus:
                __rec.unlink()
            _rec.state = "Cancelled"
    
    def review(self):
        for _rec in self:
            _employees = self.env['hr.employee'].search([])
            for _emp_rec in _employees:
                _employee_card = self.env['employee_card'].search([('employee_id','=',_emp_rec.id),
                                                 ('date','<',_rec.date)], limit=1)
                _basic_salary = self._get_basic_salary(_employee_card)
                _bonus = self._calculate_bonus(_emp_rec, _basic_salary)
                _res = self.env['employee_bonus'].create({
                    'employee_id':_emp_rec.id,
                    'batch_id': _rec.id,
                    'qualitative_group_id':_emp_rec.x_qualitative_group_id.id,
                    'current_basic_salary': _basic_salary,
                    'periodic_bonus': _bonus['periodic_bonus'],
                    'special_bonus': _bonus['special_bonus'],
                    'exceptional_bonus': _bonus['exceptional_bonus'],
                    'new_basic_salary': _bonus['_new_salary'],
                })

                # if _employee_card:
                #     self._upsert_employee_card(_employee_card, _rec.date, _bonus['_new_salary'])

        _rec.state = "In Review"

    def confirm(self):
        for _rec in self:

            for __rec in _rec.employee_bonus:
                _employee_card = self.env['employee_card'].search([('employee_id','=',__rec.employee_id.id),
                                                 ('date','<',_rec.date)], limit=1)
                
                if _employee_card:
                    self._upsert_employee_card(_employee_card, _rec.date, __rec.new_basic_salary)

            _rec.state = "Confirmed"


    def rerun(self):
        for _rec in self:
            for __rec in _rec.employee_bonus:
                __rec.unlink()

        self.review()

        #     _employees = self.env['hr.employee'].search([])
        #     for _emp_rec in _employees:
        #         _res = self.env['employee_bonus'].create({
        #             'employee_id':_emp_rec.id,
        #             'batch_id': _rec.id,
        #             'qualitative_group_id':_emp_rec.x_qualitative_group_id.id,
        #         })
        # _rec.state = "In Review"


    def _get_basic_salary(self, employee_card=False):
        
        # _rec = self.env['employee_card'].search([('employee_id','=',employee_id.id),
        #                                          ('date','<',date)], limit=1)
        
        if not employee_card:
            return 0.0
        
        _res = employee_card.basic_salary

        return _res
    
    def _calculate_bonus(self, employee_id=False, basic_salary=0.0):
        
        _res = {
            'periodic_bonus':0.0,
            'special_bonus':0.0,
            'exceptional_bonus':0.0,
            '_new_salary': 0.0,
        }
        
        if not employee_id:
            return _res
    
        _degree = employee_id.x_job_degree_id
        if _degree:
            _degree = _degree.name
        else:
            _degree = None
        
        _rec = self.env['bonus_matrix'].search([('job_degree','=',_degree)], limit=1)
        
        if not _rec:
            return _res
        
        _periodic_bonus_percent = _rec.periodic_bonus_percent
        _special_bonus_percent = _rec.special_bonus_percent
        _exceptional_bonus = _rec.exceptional_bonus_degrees
        _minimum = _rec.minimum
        _maximum = _rec.maximum
        if not _periodic_bonus_percent:
            _periodic_bonus_percent=0.0
        
        if not _special_bonus_percent:
            _special_bonus_percent=0.0
        
        if not _exceptional_bonus:
            _exceptional_bonus=0.0
        
        _periodic_bonus_calc = (_periodic_bonus_percent/100) * basic_salary
        if _minimum and _periodic_bonus_calc < _minimum:
            _periodic_bonus_calc = _minimum
        
        if _maximum and _periodic_bonus_calc > _maximum:
            _periodic_bonus_calc = _maximum

        _special_bonus_calc = (_special_bonus_percent/100) * basic_salary

        _new_salary = basic_salary + _periodic_bonus_calc + _special_bonus_calc + _exceptional_bonus
        
        _res = {
            'periodic_bonus': _periodic_bonus_calc,
            'special_bonus': _special_bonus_calc,
            'exceptional_bonus': _exceptional_bonus,
            '_new_salary': _new_salary,
        }

        return _res

    def _upsert_employee_card(self, employee_card=False, date=False, new_basic_salary=0.0):
        
        if not date:
            return False
        
        if employee_card:
            employee_card.active = False

        self.env['employee_card'].create({
            'employee_id': employee_card.employee_id.id,
            'job_degree_id': employee_card.employee_id.x_job_degree_id.id,
            'date': date,
            'basic_salary': new_basic_salary,
            'job_id': employee_card.employee_id.job_id.id,
        })


