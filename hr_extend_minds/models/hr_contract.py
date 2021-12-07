# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class hr_contract(models.Model):
    _inherit = 'hr.contract'
    

    bonus = fields.Monetary(string="Bonus", index=True, tracking=True)
    bonus_text = fields.Char(string="Bonus Text", index=True, tracking=True)
    basic_text = fields.Char(string="Basic Text", index=True, tracking=True)
    equal_degree = fields.Selection([('الأولى', 'الأولى'),
                                    ('الثانية', 'الثانية'),
                                    ('الثالثة', 'الثالثة'),
                                    ('الرابعة', 'الرابعة'),
                                    ('الخامسة', 'الخامسة'),
                                    ('السادسة', 'السادسة'),
                                    ('عالية', 'عالية'),
                                    ('ممتازة', 'ممتازة'),
                                    ('مدير عام', 'مدير عام'),
                                    ('عقد مؤقت', 'عقد مؤقت'),
                                    ('أجر مقابل عمل', 'أجر مقابل عمل'),
                                     ], string="Equal Degree", index=True, tracking=True)
    
    sector = fields.Char(related="employee_id.x_sector_name", string="Sector")
    public_administration = fields.Char(related="employee_id.x_public_administration_name", string="Public Administration")
    administration = fields.Char(related="employee_id.x_administration_name", string="Administration")
    section = fields.Char(related="employee_id.x_section_name", string="Section")
    receiving_work_date = fields.Date(related="employee_id.x_receiving_work_date", string="Receive Work Date")
    qualitative_group_id = fields.Many2one(related="employee_id.x_qualitative_group_id", string="Qualitative Group")
    

    national_id_ar = fields.Char(compute="_get_national_id_ar")
    wage_ar = fields.Char(compute="_get_wage_ar")
    bonus_ar = fields.Char(compute="_get_bonus_ar")
    current_dt_ar = fields.Char(compute="_get_current_dt_ar")
    bonus_text_ar = fields.Char(compute="_get_bonus_text_ar")
    start_date_ar = fields.Char(compute="_get_start_date_ar")
    end_date_ar = fields.Char(compute="_get_end_date_ar")
    name_ar = fields.Char(compute="_get_name_ar")
    birthday_ar = fields.Char(compute="_get_birthday_ar")
    address_ar = fields.Char(compute="_get_address_ar")
    current_day_ar = fields.Char(compute="_get_current_day_ar")
    sector_ar = fields.Char(compute="_get_sector_ar")
    #image_128_txt = fields.Char(compute="_get_image_128_txt")


    def _get_numbers_ar(self, _text=""):
        _text = _text.replace('1','١').replace('2','٢').replace('3','٣').replace('4','٤').replace('5','٥').replace('6','٦').replace('7','٧').replace('8','٨').replace('9','٩').replace('0','٠')
        _text = _text.replace('Saturday','السبت').replace('Sunday','الأحد').replace('Monday','الاثنين').replace('Tuesday','الثلاثاء').replace('Wednesday','الأربعاء').replace('Thursday','الخميس').replace('Friday','الجمعة')
        return _text

    def _get_sector_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec.sector.replace('القطاع ','').replace('قطاع ','')
            if str(_res) == "False":
                _res = ""
            _rec.sector_ar = str(_res)
        return str(_res)
    
    def _get_name_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(_rec.name)
            if str(_res) == "False":
                _res = ""
            _rec.name_ar = str(_res)
        return str(_res)
    
    # def _get_image_128_txt(self):
    #     _res = ""
    #     for _rec in self:
    #         _res = _rec.employee_id.image_128
    #         if str(_res) == "False":
    #             _res = ""
    #         _rec.image_128_txt = str(_res)
    #     return str(_res)

    def _get_national_id_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(_rec.employee_id.identification_id)
            if str(_res) == "False":
                _res = ""
            _rec.national_id_ar = str(_res)
        return str(_res)
    
    def _get_wage_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(str(_rec.wage))
            if str(_res) == "False":
                _res = ""
            _rec.wage_ar = str(_res)
        return str(_res)

    def _get_bonus_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(str(_rec.bonus))
            if str(_res) == "False":
                _res = ""
            _rec.bonus_ar = str(_res)
        return str(_res)

    def _get_current_dt_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(_rec.create_date.strftime('%d-%m-%Y'))
            if str(_res) == "False":
                _res = ""
            _rec.current_dt_ar = str(_res)
        return str(_res)

    def _get_bonus_text_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(_rec.bonus_text)
            if str(_res) == "False":
                _res = ""
            _rec.bonus_text_ar = str(_res)
        return str(_res)

    def _get_start_date_ar(self):
        _res = ""
        for _rec in self:
            if _rec.date_start:
                _res = _rec._get_numbers_ar(_rec.date_start.strftime('%d-%m-%Y'))
                if str(_res) == "False":
                    _res = ""
        _rec.start_date_ar = str(_res)
        return str(_res)

    def _get_end_date_ar(self):
        _res = ""
        for _rec in self:
            if _rec.date_end:
                _res = _rec._get_numbers_ar(_rec.date_end.strftime('%d-%m-%Y'))
                if str(_res) == "False":
                    _res = ""
        _rec.end_date_ar = str(_res)
        return str(_res)

    def _get_birthday_ar(self):
        _res = ""
        for _rec in self:
            if _rec.employee_id.birthday:
                _res = _rec._get_numbers_ar(_rec.employee_id.birthday.strftime('%d-%m-%Y'))
                if str(_res) == "False":
                    _res = ""
        _rec.birthday_ar = str(_res)
        return str(_res)

    def _get_address_ar(self):
        _res = ""
        for _rec in self:
            _res = _rec._get_numbers_ar(_rec.employee_id.address_home_id.name)
            if str(_res) == "False":
                _res = ""
            _rec.address_ar = str(_res)
        return str(_res)

    def _get_current_day_ar(self):
        _res = ""
        for _rec in self:
            _res = self._get_numbers_ar(_rec.create_date.strftime('%A'))
            if str(_res) == "False":
                _res = ""
            _rec.current_day_ar = str(_res)
        return str(_res)


    