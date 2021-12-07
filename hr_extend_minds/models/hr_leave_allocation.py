# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date, timedelta, datetime
import math

import logging

_logger = logging.getLogger(__name__)


class hr_leave_allocation(models.Model):
    _inherit = 'hr.leave.allocation'


    def allocate_emp_leaves_begin_year(self):

        _emp_recs = self.env['hr.employee'].sudo().search([])
        _logger.info("hr_leave_allocation allocate_emp_leaves_begin_year _emp_recs : " + str(_emp_recs))
        
        for _emp_rec in _emp_recs:
            
            self.allocate_AL(_emp_rec)
        
    def allocate_AL(self, _emp=False):
        
        if _emp == False:
            return False
        
        _emp_age = _emp.x_age
        _emp_oldest_hiring_date = _emp.x_oldest_hiring_date
        _emp_receiving_work_date = _emp.x_receiving_work_date
        _emp_birthday = _emp.birthday
        _current_date = date.today()
        _current_year = _current_date.year
        _al_code = "AL" + _current_year

        _al_id = self.get_leave_type_id(_al_code)

        if not _emp_oldest_hiring_date or not _emp_birthday:
            return False
        
        if not _al_id:
            return False

        _emp_allocated_leaves = self.env['hr.leave.allocation'].search([('employee_id','=',_emp.id),
                                                        ('holiday_status_id','=',_al_id),
                                                        ('state','=','validate')])

        _number_of_days = 0
        for _emp_allocated_rec in _emp_allocated_leaves:
            _number_of_days += _emp_allocated_rec.number_of_days

        _date_after_10_years = _emp_oldest_hiring_date + timedelta(years=10)
        _date_after_10_years_year = _date_after_10_years.year
        _emp_birthday_after_49_years = _emp_birthday + timedelta(years=49)
        _emp_birthday_after_49_years_year = _emp_birthday_after_49_years.year
        _emp_receiving_work_date_year = _emp_receiving_work_date.year

        _final_allocated_days = 0

        if _emp_age < 49:
            if _date_after_10_years_year == _current_year:
                _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
                _remain_days_in_current_year = (_end_current_year_date - _date_after_10_years).days
                _remain_30_days_in_current_year = _remain_days_in_current_year/365
                _remain_21_days_in_current_year = 1 - _remain_30_days_in_current_year
                _final_allocated_days = (21*_remain_21_days_in_current_year) + (30*_remain_30_days_in_current_year)
                _final_allocated_days = math.ceil(_final_allocated_days)
            
            elif _date_after_10_years_year < _current_year:
                _final_allocated_days = 30
            
            elif _date_after_10_years_year > _current_year:
                if _current_year > _emp_receiving_work_date_year:
                    _final_allocated_days = 21
                else:
                    _final_allocated_days = 15
        
        elif _emp_age >= 49:
            if _emp_birthday_after_49_years_year == _current_year:
                _end_current_year_date = datetime.strptime('{0}-12-31'.format(_current_year), '%Y-%m-%d').date()
                _remain_days_in_current_year = (_end_current_year_date - _emp_birthday_after_49_years).days
                _remain_50_days_in_current_year = _remain_days_in_current_year/365
                _remain_49_days_in_current_year = 1 - _remain_50_days_in_current_year
                _final_allocated_days = (30*_remain_49_days_in_current_year) + (45*_remain_50_days_in_current_year)
                _final_allocated_days = math.ceil(_final_allocated_days)
            
            else:
                _final_allocated_days = 45

        _logger.info("hr_leave_allocation _allocate_AL _final_allocated_days : " + str(_final_allocated_days))
            
        _final_allocated_days = _final_allocated_days - _number_of_days

        _logger.info("hr_leave_allocation _allocate_AL _emp.id : " + str(_emp.id))
        _logger.info("hr_leave_allocation _allocate_AL _number_of_days : " + str(_number_of_days))
        _logger.info("hr_leave_allocation _allocate_AL _final_allocated_days : " + str(_final_allocated_days))

        _result = self.env['hr.leave.allocation'].create({
            'employee_id': _emp.id,
            'number_of_days': _final_allocated_days,
            'holiday_status_id': _al_id,
        })

        _result.action_approve()

    def get_leave_type_id(self, _leave_type_code=False):
        
        if _leave_type_code == False:
            return False
        
        _leave_type_rec = self.env['hr.leave.type'].searh([('code','=',_leave_type_code)])
        for _rec in _leave_type_rec:
            _leave_type_id = _rec.id
            return _leave_type_id

        return False
