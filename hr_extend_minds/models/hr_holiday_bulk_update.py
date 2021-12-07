# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date, timedelta
import calendar
from calendar import monthrange
from dateutil.relativedelta import *

import logging

_logger = logging.getLogger(__name__)


class hr_holiday_bulk_update(models.Model):
    _name = 'hr_holiday_bulk_update'
    _description = 'HR Holidays Bulk Update'
    _order = 'id DESC'


    name = fields.Char(string='Holiday' ,index=True, required=True, tracking=True)
    start_date = fields.Date(string='Start Date',index=True, required=True)
    end_date = fields.Date(string='End Date', index=True, required=True)
    is_deducted = fields.Boolean(string="Is Deducted ?", index=True, required=True)
    state = fields.Selection([ ('New', 'New'),('Submit','Submit'),('Completed','Completed') ], string='Status', default="New", index=True)
    number_of_days = fields.Integer(string="Number Of Days", store=True, index=True, compute="_number_of_days")
    hr_holiday_bulk_update_employee = fields.One2many('hr_holiday_bulk_update_employee', 'hr_holiday_bulk_update_id', string="Bulk Update Employee")
    
    def submit_bulk(self):

        for _rec in self:
            _rec.state = "Submit"

    def run_bulk(self):

        _emp_recs = self.env['hr.employee'].sudo().search([('x_work_schedule_type','=','Morning')])
        _logger.info("hr_holiday_bulk_update run_bulk _emp_recs : " + str(_emp_recs))
        _current_date = date.today()
        _current_year = _current_date.year
        _al_code = "AL" + str(_current_year)
        _is_year_odd = _current_year % 2
        _fl_code = "FL01"
        _ebal_code = "EBAL2009"
        _last_even_year = False
        _leyl_code = False
        _ovl_code = "OVL01"

        _ovl_leave_type_rec = self.env['hr.leave.type'].search([('code', '=', _ovl_code)])
        _al_leave_type_rec = self.env['hr.leave.type'].search([('code','=',_al_code)])
        _leyl_leave_type_rec = False
        if _leyl_code:
            _leyl_leave_type_rec = self.env['hr.leave.type'].search([('code','=',_leyl_code)])

        _ebal_leave_type_rec = self.env['hr.leave.type'].search([('code','=',_ebal_code)])
        _fl_leave_type_rec = self.env['hr.leave.type'].search([('code','=',_fl_code)])

        if _is_year_odd != 0:
            _last_even_year = _current_year - 1
            _leyl_code = "AL" + str(_last_even_year)

        for _emp_rec in _emp_recs:

            if self.is_deducted:
                
                _al_emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp_rec.id),
                                                            ('holiday_status_id','=',_al_leave_type_rec[0].id),
                                                            ('state','=','validate')])
                
                _leyl_emp_allocated_leaves = False
                if _leyl_leave_type_rec:
                    _leyl_emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp_rec.id),
                                                            ('holiday_status_id','=',_leyl_leave_type_rec[0].id),
                                                            ('state','=','validate')])

                _ebal_emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp_rec.id),
                                                            ('holiday_status_id','=',_ebal_leave_type_rec[0].id),
                                                            ('state','=','validate')])

                _fl_emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp_rec.id),
                                                            ('holiday_status_id','=',_fl_leave_type_rec[0].id),
                                                            ('state','=','validate')])

                _al_number_of_days = 0
                _ebal_number_of_days = 0
                _leyl_number_of_days = 0
                _fl_number_of_days = 0

                if _al_emp_allocated_leaves:
                    _al_number_of_days = _al_emp_allocated_leaves[0].number_of_days
                
                if _leyl_emp_allocated_leaves:
                    _leyl_number_of_days = _leyl_emp_allocated_leaves[0].number_of_days
                
                if _ebal_emp_allocated_leaves:
                    _ebal_number_of_days = _ebal_emp_allocated_leaves[0].number_of_days
                
                if _fl_emp_allocated_leaves:
                    _fl_number_of_days = _fl_emp_allocated_leaves[0].number_of_days


                try:
                    if _al_number_of_days > 0:
                        _leave_rec = self.env["hr.leave"].create({
                            'holiday_status_id':_al_leave_type_rec[0].id,
                            'request_date_from':self.start_date,
                            'request_date_to':self.end_date,
                            'date_from':self.start_date,
                            'date_to':self.end_date,
                            'state':'draft',
                            'number_of_days': self.number_of_days,
                            'employee_id':_emp_rec.id
                        })

                        _leave_rec.action_confirm()
                        _leave_rec.action_approve()
                
                    elif _leyl_number_of_days > 0:
                        _leave_rec = self.env["hr.leave"].create({
                            'holiday_status_id':_leyl_leave_type_rec[0].id,
                            'request_date_from':self.start_date,
                            'request_date_to':self.end_date,
                            'date_from':self.start_date,
                            'date_to':self.end_date,
                            'state':'draft',
                            'number_of_days': self.number_of_days,
                            'employee_id':_emp_rec.id
                        })

                        _leave_rec.action_confirm()
                        _leave_rec.action_approve()

                    elif _ebal_number_of_days > 0:
                        _leave_rec = self.env["hr.leave"].create({
                            'holiday_status_id':_ebal_leave_type_rec[0].id,
                            'request_date_from':self.start_date,
                            'request_date_to':self.end_date,
                            'date_from':self.start_date,
                            'date_to':self.end_date,
                            'state':'draft',
                            'number_of_days': self.number_of_days,
                            'employee_id':_emp_rec.id
                        })

                        _leave_rec.action_confirm()
                        _leave_rec.action_approve()
                    
                    elif _fl_number_of_days > 0:
                        _leave_rec = self.env["hr.leave"].create({
                            'holiday_status_id':_fl_leave_type_rec[0].id,
                            'request_date_from':self.start_date,
                            'request_date_to':self.end_date,
                            'date_from':self.start_date,
                            'date_to':self.end_date,
                            'state':'draft',
                            'number_of_days': self.number_of_days,
                            'employee_id':_emp_rec.id
                        })

                        _leave_rec.action_confirm()
                        _leave_rec.action_approve()
                
                except Exception as ex:
                    self.env["hr_holiday_bulk_update_employee"].create({
                        'hr_holiday_bulk_update_id':self.id,
                        'employee_id':_emp_rec.id,
                        'desc':str(ex),
                    })

                    self.env.cr.commit()
            
            else:
                
                try:
                    if _ovl_leave_type_rec:
                        _leave_rec = self.env["hr.leave"].create({
                                    'holiday_status_id':_ovl_leave_type_rec[0].id,
                                    'request_date_from':self.start_date,
                                    'request_date_to':self.end_date,
                                    'date_from':self.start_date,
                                    'date_to':self.end_date,
                                    'state':'draft',
                                    'number_of_days': self.number_of_days,
                                    'employee_id':_emp_rec.id
                                })
                        
                        

                        _leave_rec.action_confirm()
                        _leave_rec.action_approve()
                
                except Exception as ex:
                    self.env["hr_holiday_bulk_update_employee"].create({
                        'hr_holiday_bulk_update_id':self.id,
                        'employee_id':_emp_rec.id,
                        'desc':str(ex),
                    })

                    self.env.cr.commit()

                    



        self.state = "Completed"
            

    def make_as_draft(self):

        for _rec in self:
            _rec.state = "New"

    @api.depends("start_date", "end_date")
    def _number_of_days(self):
        for _rec in self:
            if not _rec.start_date and not _rec.end_date:
                return False
            
            _days_diff = (_rec.end_date - _rec.start_date).days + 1
            _number_of_days = 0

            for _r in range(_days_diff):
                _calendar_day = calendar.day_name[(_rec.start_date + timedelta(days=_r)).weekday()]

                if _calendar_day != "Friday" and _calendar_day != "Saturday" :
                    _number_of_days = _number_of_days + 1
            _rec.number_of_days = _number_of_days
            return _rec.number_of_days


    _sql_constraints = [('constrainname', 'UNIQUE (name)', 'This name is already exists'),
                         ('constrainname', 'UNIQUE (start_date)', 'This start date is already exists'),
                         ('constrainname', 'UNIQUE (end_date)', 'This end date is already exists')]