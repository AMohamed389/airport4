# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
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


class hrleaveextend(models.Model):

    _inherit = 'hr.leave'

    x_sector_name = fields.Char(related="employee_id.x_sector_name", index=True)
    x_public_administration_name = fields.Char(related="employee_id.x_public_administration_name", index=True)
    x_administration_name = fields.Char(related="employee_id.x_administration_name", index=True)
    x_section_name = fields.Char(related="employee_id.x_section_name", index=True)
    x_staff_id = fields.Char(related="employee_id.x_staff_id", index=True)
    x_issuer = fields.Selection([('تأمين مصر للطيران','تأمين مصر للطيران'),
                                ('تأمين صحي','تأمين صحي'),
                                ('DMS تأمين','DMS تأمين')],string="Source", index=True, tracking=True)
    x_work_schedule_type = fields.Selection(related="employee_id.x_work_schedule_type", index=True)
    x_resource_calendar_name = fields.Char(string="Schedule Name", related="employee_id.resource_calendar_id.name", index=True)
    x_half_shift_leave_flg = fields.Boolean(string="Half Shift Leave", index=True, tracking=True)
    x_leave_type_name  = fields.Char(string="Leave Type Name", related="holiday_status_id.name", index=True)
    x_leave_type_code = fields.Char(string="Leave Type Code", related="holiday_status_id.code", index=True)


    def write(self, vals):

        result = super(hrleaveextend, self).write(vals)
        _logger.info(str("hr_leave write result : ") + str(result))

        for _rec in self:
            _rec.validate_after_sl()
            _rec.validate_fl(vals)
            _rec.validate_first_six_months(vals)
            _rec.validate_cl(vals)
            _rec.validate_dms_sl(vals)
            _rec.validate_rrl(vals)
            _rec.validate_oocl()
            _rec.validate_osl()
            _rec.validate_mscl()
            _rec.validate_snfpl9001()
            _rec.validate_snfpl18002()
            _rec.validate_snfpl18003()
            _rec.validate_snfpl18004()
            _rec.validate_ml()
            
        return result
                
    def validate_no_leaves_after_sl(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _gender = _employee.gender
        _number_of_days = self.number_of_days

        if not _employee or not _leave_type_rec:
            return False

    def validate_fl(self, vals):
        
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _number_of_days = self.number_of_days
        _half_leave_flg = self.x_half_shift_leave_flg
        _work_schedule_type = self.x_work_schedule_type

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "FL01":
            
            _todays_date = date.today()

            _employee_leaves = self.get_total_leaves_days(_leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 60:
                raise ValidationError(_("Year {0} consumed > 60 days for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))

    def validate_first_six_months(self, vals):

        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _number_of_days = self.number_of_days
        _receiving_work_date = _employee.x_receiving_work_date
        #_receiving_work_date_year = _receiving_work_date.year
        _todays_date = date.today()
        _current_year = _todays_date.year
        _current_casual_leave_code = "CL" + str(_current_year)
        _current_annual_leave_code = "AL" + str(_current_year)

        if not _employee or not _leave_type_rec:
            return False

        if not _receiving_work_date:
            raise ValidationError(_("Receive Work Date field is empty for employee name : {0}, code : {1} !.".format(_employee.name,_employee.x_staff_id)))

        _months_diff = self.diff_month(_todays_date, _receiving_work_date)

        if _months_diff >= 6:
            return True
        
        if _current_annual_leave_code == _leave_code and _months_diff < 6:
            raise ValidationError(_("Year {0} cannot take {1} in first 6 months !.".format(str(date.today().year), _leave_type_rec.name)))

        if _current_casual_leave_code !=  _leave_code and _months_diff < 6:
            raise ValidationError(_("Year {0} only casual and annual leaves are allowaed for receiving work date < 6 !.".format(str(date.today().year))))
        
        if _number_of_days > 3 and _current_casual_leave_code ==  _leave_code:
            raise ValidationError(_("Year {0} consumed > 3 days for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))

        _employee_leaves = self.get_total_leaves_days(_leave_code=_leave_code)
        _total_number_of_days = _employee_leaves['total_number_of_days']
        
        if _total_number_of_days > 3 and _current_casual_leave_code ==  _leave_code :
            raise ValidationError(_("Year {0} consumed > 3 days for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))
            
    def validate_cl(self, vals):

        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _number_of_days = self.number_of_days
        #_receiving_work_date_year = _receiving_work_date.year
        _todays_date = date.today()
        _current_year = _todays_date.year
        _current_casual_leave_code = "CL" + str(_current_year)
        _current_annual_leave_code = "AL" + str(_current_year)
        _request_date_from = self.request_date_from
        #_request_date_to = self.request_date_to

        if not _employee or not _leave_type_rec:
            return False

        if _leave_code == _current_casual_leave_code:
            
            #_days_diff = (_request_date_to - _request_date_from).days + 1

            if vals.get('number_of_days'):
                _days_diff = vals.get('number_of_days')
            else:
                _days_diff = _number_of_days

            #_logger.info("hr_leave validate_cl _days_diff : " + str(_days_diff))

            if _days_diff > 2:
                _check_third_date = _request_date_from + timedelta(days=2)
                #_logger.info("hr_leave validate_cl _check_third_date : " + str(_check_third_date))

                _calendar_day = calendar.day_name[_check_third_date.weekday()]
                #_logger.info("hr_leave validate_cl _calendar_day : " + str(_calendar_day))

                if _calendar_day != "Friday" and _calendar_day != "Saturday" :
                    raise ValidationError(_("Year {0} consumed > 2 consecutive days for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))
            
            _day_before_cl = _request_date_from - timedelta(days=1)
            _employee_leaves = self.get_total_leaves_days_for_cl(_request_date_to = _day_before_cl, _leave_code=_current_annual_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 0:
                raise ValidationError(_("Year {0} cannot take casual leave after annual leave for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))

            _employee_leaves = self.get_total_leaves_days_for_cl(_request_date_to = _day_before_cl, _leave_code=_current_casual_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 0:
                raise ValidationError(_("Year {0} cannot take casual leaves after casual leave for leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))
        
    def validate_dms_sl(self, vals):

        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _number_of_days = self.number_of_days        
        _todays_date = date.today()
        _current_year = _todays_date.year
        _sick_dms_leave_code = "SDMSL01"
        _request_date_from = self.request_date_from
        _request_date_to = self.request_date_to

        if not _employee or not _leave_type_rec:
            return False
        

        _receiving_work_date = _employee.x_receiving_work_date
        if not _receiving_work_date:
            raise ValidationError(_("Receive Work Date field is empty for employee name : {0}, code : {1} !.".format(_employee.name,_employee.x_staff_id)))

        _receiving_work_date_year = _receiving_work_date.year

        if _leave_code == _sick_dms_leave_code:
            
            if vals.get('number_of_days'):
                _days_diff = vals.get('number_of_days')
            else:
                _days_diff = _number_of_days

            #_logger.info("hr_leave validate_cl _days_diff : " + str(_days_diff))

            # if _days_diff > 3:
            #     raise ValidationError("Consumed > 3 consecutive days for leave {0} !.".format(_leave_type_rec.name))
            
            if _days_diff > 15:
                raise ValidationError("Consumed > 15 consecutive days for leave {0} !.".format(_leave_type_rec.name))
            

            _day_before_dmssl = _request_date_from - timedelta(days=1)
            _employee_leaves = self.get_total_leaves_days_for_cl(_request_date_to = _day_before_dmssl, _leave_code=_sick_dms_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 2:
                raise ValidationError(_("Year {0} cannot take DMS sick leave after DMS sick leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))


            # _request_date_from_year = _request_date_from.year
            # _request_date_to_year = _request_date_to.year

            # _request_date_from_month = _request_date_from.month
            # _request_date_to_month = _request_date_to.month

            # _number_of_days_to_month = monthrange(_request_date_to_year, _request_date_to_month)[1]

            # _check_from_dt = str(_request_date_from_year) + "-" + str(_request_date_from_month) + "-01"
            # _check_to_dt = str(_request_date_to_year) + "-" + str(_request_date_to_month) + "-" + str(_number_of_days_to_month)

            # if _request_date_from_month == _request_date_to_month and _request_date_from_year == _request_date_to_year:
            #     _employee_leaves = self.get_total_leaves_days(_request_date_from = _check_from_dt ,_request_date_to = _check_to_dt, _leave_code=_sick_dms_leave_code)
            #     _total_number_of_days = _employee_leaves['total_number_of_days']

            #     if _total_number_of_days > 15:
            #         raise ValidationError("Consumed > 15 DMS leaves for leave {0} !.".format(_leave_type_rec.name))
        
    def validate_rrl(self, vals):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _days_diff = self.number_of_days

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "RRL01":
            
            if vals.get('number_of_days'):
                _days_diff = vals.get('number_of_days')

            if _days_diff != 22:
                raise ValidationError(_("Religion leave must be 30 days for leave {0} !.".format(_leave_type_rec.name)))

            _employee_leaves = self.get_total_leaves_days(_request_date_from="1960-01-01",_request_date_to="2100-12-31", _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 22:
                raise ValidationError(_("Consumed > 30 days for leave {0} !.".format(_leave_type_rec.name)))
    
    def validate_oocl(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _gender = _employee.gender
        _number_of_days = self.number_of_days

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "OCCL01":
            
            if _gender != "female" and _gender != "أنثى":
                 raise ValidationError(_("this leave is valid only for female for leave {0} !.".format(_leave_type_rec.name)))
            
            _employee_leaves = self.get_total_leaves_days(_request_date_from="1960-01-01",_request_date_to="2100-12-31", _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 1584:
                raise ValidationError(_("Consumed > 6 years for leave {0} !.".format(_leave_type_rec.name)))

    def validate_ml(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _gender = _employee.gender
        _number_of_days = self.number_of_days

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "ML01":
            
            if _gender != "female" and _gender != "أنثى":
                 raise ValidationError(_("this leave is valid only for female for leave {0} !.".format(_leave_type_rec.name)))
            
            _employee_leaves = self.get_total_leaves_days(_request_date_from="1960-01-01",_request_date_to="2100-12-31", _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 66:
                raise ValidationError(_("Consumed > 6 years for leave {0} !.".format(_leave_type_rec.name)))
            
            if _number_of_days != 22:
                raise ValidationError(_("Consumed > 6 years for leave {0} !.".format(_leave_type_rec.name)))

            _leaves_recs = self.env['hr.leave'].search_count([('request_date_from','>=',"1960-01-01"),
                        ('request_date_to','<=',"2100-12-31"),('state','=','validate'),
                        ('holiday_status_id','=',_leave_type_rec.id),
                        ('employee_id','=',_employee)])

            if _leaves_recs > 3:
                raise ValidationError(_("Consumed > 3 times for leave {0} !.".format(_leave_type_rec.name)))

    def validate_osl(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "OSL01":
            
            _employee_leaves = self.get_total_leaves_days(_request_date_from="1960-01-01",_request_date_to="2100-12-31", _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 1056:
                raise ValidationError(_("Consumed > 4 years for leave {0} !.".format(_leave_type_rec.name)))

    def validate_mscl(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "MSCL01":
            
            _employee_leaves = self.get_total_leaves_days(_request_date_from="1960-01-01",_request_date_to="2100-12-31", _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 1056:
                raise ValidationError(_("Consumed > 4 years for leave {0} !.".format(_leave_type_rec.name)))

    def validate_snfpl9001(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "SNFPL9001":
            
            _sick_90_days_leaves = self.calc_90_sick_days_for_employee()
            _sick_90days_start_dt = _sick_90_days_leaves['_sick_90days_start_dt']
            _sick_90days_end_dt = _sick_90_days_leaves['_sick_90days_end_dt']

            _employee_leaves = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_code)
            _total_number_of_days = _employee_leaves['total_number_of_days']
            
            if _total_number_of_days > 66:
                raise ValidationError(_("Consumed > 90 days for leave {0} !.\n\nStart Date : {1}\nEnd Date : {2}"
                                    .format(_leave_type_rec.name, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt))))

    def validate_snfpl18002(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "SNFPL18002":
            
            _leave_type_code_snfpl9001 = "SNFPL9001"
            _leave_type_name_snfpl9001 = False
            _leave_type_snfpl9001_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl9001)])
            for __leave_type_snfpl9001_rec in _leave_type_snfpl9001_rec:
                _leave_type_name_snfpl9001 = __leave_type_snfpl9001_rec.name
            
            _sick_90_days_leaves = self.calc_90_sick_days_for_employee()
            _sick_90days_start_dt = _sick_90_days_leaves['_sick_90days_start_dt']
            _sick_90days_end_dt = _sick_90_days_leaves['_sick_90days_end_dt']

            _employee_leaves_90_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_type_code_snfpl9001)
            _total_number_of_consumed_90_days = _employee_leaves_90_days['total_number_of_days']
            
            if _total_number_of_consumed_90_days < 66:
                raise ValidationError(_("""Consumed < 90 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl9001, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(66 - _total_number_of_consumed_90_days))))
            
            
            _sick_90_days_leaves = self.calc_90_sick_days_for_employee()
            _sick_90days_start_dt = _sick_90_days_leaves._sick_90days_start_dt
            _sick_90days_end_dt = _sick_90_days_leaves._sick_90days_end_dt

            _employee_leaves_18002_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_code)
            _total_number_of_consumed_18002_days = _employee_leaves_18002_days['total_number_of_days']
            
            if _total_number_of_consumed_18002_days > 132:
                raise ValidationError(_("""Consumed > 180 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                    """
                                    .format(_leave_type_rec.name, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt))))

    def validate_snfpl18003(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "SNFPL18003":
            
            _leave_type_code_snfpl9001 = "SNFPL9001"
            _leave_type_name_snfpl9001 = False
            _leave_type_snfpl9001_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl9001)])
            for __leave_type_snfpl9001_rec in _leave_type_snfpl9001_rec:
                _leave_type_name_snfpl9001 = __leave_type_snfpl9001_rec.name
            
            _sick_90_days_leaves = self.calc_90_sick_days_for_employee()
            _sick_90days_start_dt = _sick_90_days_leaves['_sick_90days_start_dt']
            _sick_90days_end_dt = _sick_90_days_leaves['_sick_90days_end_dt']

            _employee_leaves_90_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_type_code_snfpl9001)
            _total_number_of_consumed_90_days = _employee_leaves_90_days['total_number_of_days']
            
            if _total_number_of_consumed_90_days < 66:
                raise ValidationError(_("""Consumed < 90 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl9001, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(66 - _total_number_of_consumed_90_days))))
            
            _leave_type_code_snfpl18002 = "SNFPL18002"
            _leave_type_name_snfpl18002 = False
            _leave_type_snfpl18002_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl18002)])
            for __leave_type_snfpl18002_rec in _leave_type_snfpl18002_rec:
                _leave_type_name_snfpl18002 = __leave_type_snfpl18002_rec.name

            _employee_leaves_18002_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_code)
            _total_number_of_consumed_18002_days = _employee_leaves_18002_days['total_number_of_days']
            
            if _total_number_of_consumed_18002_days < 132:
                raise ValidationError(_("""Consumed < 132 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl18002, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(132 - _total_number_of_consumed_18002_days))))


            _employee_leaves_18003_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_code)
            _total_number_of_consumed_18003_days = _employee_leaves_18003_days['total_number_of_days']
            
            if _total_number_of_consumed_18003_days > 132:
                raise ValidationError(_("""Consumed > 180 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                    """
                                    .format(_leave_type_rec.name, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt))))

    def validate_snfpl18004(self):
        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id

        if not _employee or not _leave_type_rec:
            return False
        
        if _leave_code == "SNFPL18004":
            
            _leave_type_code_snfpl9001 = "SNFPL9001"
            _leave_type_name_snfpl9001 = False
            _leave_type_snfpl9001_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl9001)])
            for __leave_type_snfpl9001_rec in _leave_type_snfpl9001_rec:
                _leave_type_name_snfpl9001 = __leave_type_snfpl9001_rec.name
            
            _sick_90_days_leaves = self.calc_90_sick_days_for_employee()
            _sick_90days_start_dt = _sick_90_days_leaves['_sick_90days_start_dt']
            _sick_90days_end_dt = _sick_90_days_leaves['_sick_90days_end_dt']

            _employee_leaves_90_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_type_code_snfpl9001)
            _total_number_of_consumed_90_days = _employee_leaves_90_days['total_number_of_days']
            
            if _total_number_of_consumed_90_days < 66:
                raise ValidationError(_("""Consumed < 90 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl9001, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(66 - _total_number_of_consumed_90_days))))
            

            _leave_type_code_snfpl18002 = "SNFPL18002"
            _leave_type_name_snfpl18002 = False
            _leave_type_snfpl18002_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl18002)])
            for __leave_type_snfpl18002_rec in _leave_type_snfpl18002_rec:
                _leave_type_name_snfpl18002 = __leave_type_snfpl18002_rec.name

            _employee_leaves_18002_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_type_code_snfpl18002)
            _total_number_of_consumed_18002_days = _employee_leaves_18002_days['total_number_of_days']
            
            if _total_number_of_consumed_18002_days < 132:
                raise ValidationError(_("""Consumed < 132 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl18002, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(132 - _total_number_of_consumed_18002_days))))

            _leave_type_code_snfpl18003 = "SNFPL18003"
            _leave_type_name_snfpl18003 = False
            _leave_type_snfpl18003_rec = self.env['hr.leave.type'].search([('code','=',_leave_type_code_snfpl18002)])
            for __leave_type_snfpl18003_rec in _leave_type_snfpl18003_rec:
                _leave_type_name_snfpl18003 = __leave_type_snfpl18003_rec.name

            _employee_leaves_18003_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_type_code_snfpl18003)
            _total_number_of_consumed_18003_days = _employee_leaves_18003_days['total_number_of_days']
            
            if _total_number_of_consumed_18003_days < 132:
                raise ValidationError(_("""Consumed < 180 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                        \n
                                        Please consume the balance of {0} first !.
                                        Remaining Balance : {3}
                                    """
                                    .format(_leave_type_name_snfpl18003, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt), str(132 - _total_number_of_consumed_18003_days))))

            
            _employee_leaves_18004_days = self.get_total_leaves_days(_request_date_from=_sick_90days_start_dt, _request_date_to=_sick_90days_end_dt, _leave_code=_leave_code)
            _total_number_of_consumed_18004_days = _employee_leaves_18004_days['total_number_of_days']
            
            if _total_number_of_consumed_18004_days > 132:
                raise ValidationError(_("""Consumed > 180 days for leave {0} !.\n
                                        Start Date : {1}
                                        End Date : {2}
                                    """
                                    .format(_leave_type_rec.name, str(_sick_90days_start_dt),
                                    str(_sick_90days_end_dt))))
        
    def get_total_leaves_days(self, _current_year=date.today().year, _request_date_from=str(date.today().year) + "-01-01", _request_date_to=str(date.today().year) + "-12-31", _leave_code=False):
        
        if not _leave_code:
            return _leave_code
        
        _leave_type_rec = self.env['hr.leave.type'].search([('code','=',_leave_code)],limit=1)
        #_logger.info("hrleaveextend get_total_leaves_days _leave_type_rec : " + str(_leave_type_rec))

        if not _leave_type_rec:
            return _leave_type_rec

        _dict = {}
        _total_duration_days = 0
        _leaves_recs = self.env['hr.leave'].search([('request_date_from','>=',_request_date_from),
                        ('request_date_to','<=',_request_date_to),('state','=','validate'),
                        ('holiday_status_id','=',_leave_type_rec.id),
                        ('employee_id','=',self.employee_id.id)])
        
        #_logger.info("hrleaveextend get_total_leaves_days _leaves_recs : " + str(_leaves_recs))

        for _rec in _leaves_recs:
            _dict[_rec.holiday_status_id.code] = {
                'request_date_from':_rec.request_date_from,
                'request_date_to':_rec.request_date_to,
                'number_of_days':_rec.number_of_days
            }
            _total_duration_days += _rec.number_of_days
        
        _dict['total_number_of_days'] = _total_duration_days
        _dict['employee_id'] = self.employee_id.id

        #_logger.info("hrleaveextend get_total_leaves_days _dict : " + str(_dict))

        return _dict

    def get_total_leaves_days_for_cl(self, _request_date_to=str(date.today().year) + "-12-31", _leave_code=False):
        
        if not _leave_code:
            return _leave_code
        
        _leave_type_rec = self.env['hr.leave.type'].search([('code','=',_leave_code)],limit=1)
        #_logger.info("hrleaveextend get_total_leaves_days _leave_type_rec : " + str(_leave_type_rec))

        if not _leave_type_rec:
            return _leave_type_rec

        _dict = {}
        _total_duration_days = 0
        _leaves_recs = self.env['hr.leave'].search([('request_date_to','=',_request_date_to),
                        ('state','=','validate'),
                        ('holiday_status_id','=',_leave_type_rec.id),
                        ('employee_id','=',self.employee_id.id)])
        
        #_logger.info("hrleaveextend get_total_leaves_days _leaves_recs : " + str(_leaves_recs))

        for _rec in _leaves_recs:
            _dict[_rec.holiday_status_id.code] = {
                'request_date_from':_rec.request_date_from,
                'request_date_to':_rec.request_date_to,
                'number_of_days':_rec.number_of_days
            }
            _total_duration_days += _rec.number_of_days
        
        _dict['total_number_of_days'] = _total_duration_days
        _dict['employee_id'] = self.employee_id.id

        #_logger.info("hrleaveextend get_total_leaves_days _dict : " + str(_dict))

        return _dict

    def get_total_leaves_days_for_sl(self, _request_date_to=str(date.today().year) + "-12-31"):
        

        _dict = {}
        _total_duration_days = 0
        _leaves_recs = self.env['hr.leave'].search([('request_date_to','=',_request_date_to),
                        ('state','=','validate'),
                        ('employee_id','=',self.employee_id.id)])
        
        #_logger.info("hrleaveextend get_total_leaves_days _leaves_recs : " + str(_leaves_recs))

        for _rec in _leaves_recs:
            _dict[_rec.holiday_status_id.code] = {
                'request_date_from':_rec.request_date_from,
                'request_date_to':_rec.request_date_to,
                'number_of_days':_rec.number_of_days
            }
            _dict['leave_code'] = _rec.holiday_status_id.code
            _total_duration_days += _rec.number_of_days
        
        _dict['total_number_of_days'] = _total_duration_days
        _dict['employee_id'] = self.employee_id.id

        #_logger.info("hrleaveextend get_total_leaves_days _dict : " + str(_dict))

        return _dict

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def calc_90_sick_days_for_employee(self):

        _employee = self.employee_id

        if not _employee:
            return False

        _receiving_work_date = _employee.x_receiving_work_date
        if not _receiving_work_date:
            raise ValidationError(_("Receive Work Date field is empty for employee name : {0}, code : {1} !.".format(_employee.name,_employee.x_staff_id)))
        _receiving_work_date_year = _receiving_work_date.year
        
        _todays_date = date.today()
        # _current_year = _todays_date.year
        # _current_month = _todays_date.month
        # _current_day = _todays_date.day

        _sick_years_date = _receiving_work_date + relativedelta(years=+3)

        while _todays_date > _sick_years_date:
            _sick_years_date = _sick_years_date + relativedelta(years=+3)

        _sick_90days_start_dt = _sick_years_date - relativedelta(years=+3)
        _sick_90days_end_dt = _sick_years_date
        _dict = {
            '_sick_90days_start_dt':_sick_90days_start_dt,
            '_sick_90days_end_dt':_sick_90days_end_dt
        }
        
        return _dict

    def validate_after_sl(self):

        _leave_type_rec = self.env['hr.leave.type'].browse(self.holiday_status_id.id)
        _leave_code = _leave_type_rec.code
        _employee = self.employee_id
        _number_of_days = self.number_of_days
        _todays_date = date.today()
        _current_year = _todays_date.year
        _sick_dms_leave_code = "SDMSL01"
        _sick_sfpl_leave_code = "SFPL01"
        _sick_scml_leave_code = "SCML01"
        _sick_scsl_leave_code = "SCSL01"
        _sick_scil_leave_code = "SCIL01"
        _sick_snfpl9001_leave_code = "SNFPL9001"
        _sick_snfpl18002_leave_code = "SNFPL18002"
        _sick_snfpl18003_leave_code = "SNFPL18003"
        _sick_snfpl18004_leave_code = "SNFPL18004"
        _request_date_from = self.request_date_from
        _request_date_to = self.request_date_to

        _receiving_work_date = _employee.x_receiving_work_date
        if not _receiving_work_date:
            raise ValidationError(_("Receive Work Date field is empty for employee name : {0}, code : {1} !.".format(_employee.name,_employee.x_staff_id)))

        _receiving_work_date_year = _receiving_work_date.year

        if not _employee or not _leave_type_rec:
            return False
        

        _day_before = _request_date_from - timedelta(days=1)
        _employee_leaves = self.get_total_leaves_days_for_sl(_request_date_to = _day_before)
        _total_number_of_days = _employee_leaves['total_number_of_days']
        _leave_code_res = _employee_leaves.get("leave_code")

        if _leave_code_res:
            if _leave_code_res == "AL" + str(_current_year) or _leave_code_res == "CL" + str(_current_year) \
            or _leave_code_res == "RRL01" or _leave_code_res == "ML01" or _leave_code_res == "OCCL01" \
            or _leave_code_res == "OSL01" or _leave_code_res == "MSCL01" or _leave_code_res == "MEL01" \
            or _leave_code_res == "OVL01" :
                raise ValidationError(_("Year {0} cannot take any not sick leave after sick leave {1} !.".format(str(date.today().year), _leave_type_rec.name)))

    @api.depends('date_from', 'date_to', 'employee_id', 'x_half_shift_leave_flg')
    def _compute_number_of_days(self):
        
        for holiday in self:

            _half_leave_flg = holiday.x_half_shift_leave_flg
            _work_schedule_type = holiday.x_work_schedule_type
            _leave_code = holiday.x_leave_type_code
            _todays_date = date.today()
            _current_year = _todays_date.year
            _current_casual_leave_code = "CL" + str(_current_year)
            _current_annual_leave_code = "AL" + str(_current_year)

            if holiday.date_from and holiday.date_to:
                if _work_schedule_type == "Shift" and not _half_leave_flg and \
                (_leave_code == "FL01" or _leave_code == _current_casual_leave_code or _leave_code == _current_annual_leave_code):

                    holiday.number_of_days = (holiday._get_number_of_days(holiday.date_from, holiday.date_to, holiday.employee_id.id)['days']) * 2
                else:
                    holiday.number_of_days = holiday._get_number_of_days(holiday.date_from, holiday.date_to, holiday.employee_id.id)['days']
            else:
                holiday.number_of_days = 0

