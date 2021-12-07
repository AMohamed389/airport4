# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
import math

import logging

_logger = logging.getLogger(__name__)


class employee_leave_allocation(models.Model):
    _name = 'employee_leave_allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id DESC'

    name = fields.Char(string="Name", index=True, required=True, tracking=True)
    state = fields.Selection([
        ('Draft', 'Draft'),('Submit', 'Submit'),('Completed', 'Completed')
    ], string='Run State' ,default='Draft', index=True, tracking=True)

    active = fields.Boolean(string='Active',index=True,default=True)


    def allocate_emp_leaves_begin_year(self):

        self.state = "Submit"

        _emp_recs = self.env['hr.employee'].sudo().search([])
        _logger.info("hr_leave_allocation allocate_emp_leaves_begin_year _emp_recs : " + str(_emp_recs))
        
        for _emp_rec in _emp_recs:
            
            self.allocate_AL(_emp_rec)
            self.allocate_cl(_emp_rec)
            self.allocate_rrl(_emp_rec)
            self.allocate_occl(_emp_rec)
            self.allocate_osl(_emp_rec)
            self.allocate_mscl(_emp_rec)
            self.allocate_ml(_emp_rec)
        
        self.state = "Completed"

    def allocate_mscl(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_gender = _emp.gender
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _mscl_code = "MSCL01"

        _mscl_id = self.get_leave_type_id(_mscl_code)

        if not _mscl_id :
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_mscl_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 1056 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _mscl_id,
            })

            _result.action_approve()

    def allocate_osl(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_gender = _emp.gender
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _osl_code = "OSL01"

        _osl_id = self.get_leave_type_id(_osl_code)

        if not _osl_id :
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_osl_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 1056 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _osl_id,
            })

            _result.action_approve()

    def allocate_occl(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_gender = _emp.gender
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _occl_code = "OCCL01"

        _occl_id = self.get_leave_type_id(_occl_code)

        if not _occl_id or (_emp_gender != "female" and _emp_gender != "أنثى"):
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_occl_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 1584 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _occl_id,
            })

            _result.action_approve()

    def allocate_ml(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_gender = _emp.gender
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _ml_code = "ML01"

        _ml_id = self.get_leave_type_id(_ml_code)

        if not _ml_id or (_emp_gender != "female" and _emp_gender != "أنثى"):
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_ml_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 66 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _ml_id,
            })

            _result.action_approve()

    def allocate_cl(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _cl_code = "CL" + str(_current_year)

        _cl_id = self.get_leave_type_id(_cl_code)

        if not _cl_id:
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_cl_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 7 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _cl_id,
            })

            _result.action_approve()
 
    def allocate_AL(self, _emp=False):
        
        if _emp == False:
            return False
        
        # _logger.info("**********hr_leave_allocation _allocate_AL _emp.id : " + str(_emp.id) + " **********")
        # _logger.info("**********hr_leave_allocation _allocate_AL _emp.id : " + str(_emp.name) + " **********")
        _emp_age = _emp.x_age
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _al_code = "AL" + str(_current_year)

        _al_id = self.get_leave_type_id(_al_code)

        if not _emp_oldest_hiring_date:
            _emp_oldest_hiring_date = _emp_receiving_work_date

        if not _emp_birthday or not _emp_receiving_work_date:
            # _logger.info("hr_leave_allocation _allocate_AL _emp.name : " + str(_emp.name))
            # _logger.info("hr_leave_allocation _allocate_AL _emp_oldest_hiring_date : " + str(_emp_oldest_hiring_date))
            # _logger.info("hr_leave_allocation _allocate_AL _emp_birthday : " + str(_emp_birthday))
            # _logger.info("hr_leave_allocation _allocate_AL _emp_receiving_work_date : " + str(_emp_receiving_work_date))
            return False
        
        if not _al_id:
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_al_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days

            
        _date_after_10_years = _emp_oldest_hiring_date + relativedelta(years=+10)
        _date_after_10_years_year = _date_after_10_years.year
        _emp_birthday_after_49_years = _emp_birthday + relativedelta(years=+49)
        _emp_birthday_after_49_years_year = _emp_birthday_after_49_years.year
        _emp_receiving_work_date_year = _emp_receiving_work_date.year
        _emp_receiving_work_date_after_6_months = _emp_receiving_work_date + relativedelta(months=+6)
        _emp_receiving_work_date_after_1_year = _emp_receiving_work_date + relativedelta(months=+12)
        #_emp_delta_days_10_oldest_hiring_receiving_work_dates = (_emp_receiving_work_date_after_1_year - _date_after_10_years).days
        
        
        # _logger.info("hr_leave_allocation _allocate_AL _number_of_days : " + str(_number_of_days))
        # _logger.info("hr_leave_allocation _allocate_AL _date_after_10_years : " + str(_date_after_10_years))
        # _logger.info("hr_leave_allocation _allocate_AL _date_after_10_years_year : " + str(_date_after_10_years_year))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_birthday_after_49_years : " + str(_emp_birthday_after_49_years))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_birthday_after_49_years_year : " + str(_emp_birthday_after_49_years_year))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_receiving_work_date_year : " + str(_emp_receiving_work_date_year))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_age : " + str(_emp_age))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_receiving_work_date_after_6_months : " + str(_emp_receiving_work_date_after_6_months))
        # _logger.info("hr_leave_allocation _allocate_AL _emp_receiving_work_date_after_1_year : " + str(_emp_receiving_work_date_after_1_year))
        #_logger.info("hr_leave_allocation _allocate_AL _emp_delta_days_10_oldest_hiring_receiving_work_dates : " + str(_emp_delta_days_10_oldest_hiring_receiving_work_dates))

        _final_allocated_days = 0

        if int(_emp_age) < 49:
            if _date_after_10_years_year == _current_year and _begin_current_year_date >= _emp_receiving_work_date_after_1_year:

                _remain_days_in_current_year = (_end_current_year_date - _date_after_10_years).days
                _remain_30_days_in_current_year = _remain_days_in_current_year/365
                _remain_21_days_in_current_year = 1 - _remain_30_days_in_current_year
                _final_allocated_days = (21*_remain_21_days_in_current_year) + (30*_remain_30_days_in_current_year)
                _final_allocated_days = math.ceil(_final_allocated_days)
            
            elif _date_after_10_years_year < _current_year:
                _final_allocated_days = 30
            
            elif _date_after_10_years_year > _current_year:

                if _end_current_year_date > _emp_receiving_work_date_after_1_year:
                    _final_allocated_days = 21

                    # if _emp_delta_days_10_oldest_hiring_receiving_work_dates >= 0:
                    #     _final_allocated_days = 21
                    # else:
                    #     _final_allocated_days = 15

                elif _end_current_year_date >= _emp_receiving_work_date_after_6_months:
                    _final_allocated_days = 15
                    _delta_days = (_end_current_year_date - _emp_receiving_work_date_after_1_year).days
                    
                    _delta_days_leave = 0
                    # if _emp_delta_days_10_oldest_hiring_receiving_work_dates >= 0:
                    #     _delta_days_leave = (_delta_days/365)*30
                    # else:
                    _delta_days_leave = (_delta_days/365)*21 #TODO - 15 days
                    
                    _final_allocated_days += _delta_days_leave
                
                _final_allocated_days = math.ceil(_final_allocated_days)
                    
        
        elif int(_emp_age) >= 49:
            if _emp_birthday_after_49_years_year == _current_year:
                _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
                _remain_days_in_current_year = (_end_current_year_date - _emp_birthday_after_49_years).days
                _remain_50_days_in_current_year = _remain_days_in_current_year/365
                _remain_49_days_in_current_year = 1 - _remain_50_days_in_current_year
                _final_allocated_days = (30*_remain_49_days_in_current_year) + (45*_remain_50_days_in_current_year)
                _final_allocated_days = math.ceil(_final_allocated_days)
            
            else:
                _final_allocated_days = 45

        # _logger.info("hr_leave_allocation _allocate_AL _final_allocated_days : " + str(_final_allocated_days))
            
        _final_allocated_days = _final_allocated_days - _number_of_days

        
        # _logger.info("hr_leave_allocation _allocate_AL _number_of_days : " + str(_number_of_days))
        # _logger.info("hr_leave_allocation _allocate_AL _final_allocated_days : " + str(_final_allocated_days))

        if _final_allocated_days > 0:
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _al_id,
            })

            _result.action_approve()

    def allocate_rrl(self, _emp=False):
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _begin_current_year_date = datetime.strptime('{0}-01-01'.format(_current_year), '%Y-%m-%d').date()
        _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
        _rrll_code = "RRL01"

        _rrll_id = self.get_leave_type_id(_rrll_code)

        if not _rrll_id:
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                            ('holiday_status_id','=',_rrll_id),
                                                            ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days


        _final_allocated_days = 22 - _number_of_days

        if _final_allocated_days > 0:
            
            _result = self.env['hr.leave.allocation'].create({
                'employee_id': _emp.id,
                'number_of_days': _final_allocated_days,
                'holiday_status_id': _rrll_id,
            })

            _result.action_approve()

    def get_leave_type_id(self, _leave_type_code=False):
        
        if _leave_type_code == False:
            return False
        
        _leave_type_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code)])
        for _rec in _leave_type_rec:
            _leave_type_id = _rec.id
            return _leave_type_id

        return False





    _sql_constraints = [('constrain_name', 'UNIQUE (name)', 'The name is already exists !.')]