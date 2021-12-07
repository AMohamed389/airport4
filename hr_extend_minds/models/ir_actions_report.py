# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _

from datetime import date, datetime, time
from dateutil import parser
#import pandas as pd

import logging
_logger = logging.getLogger(__name__)

class hr_employee_report(models.Model):
    _inherit = 'ir.actions.report'




    # @api.model
    # def _render_qweb_html(self, docids, data=None):
    #     """This method generates and returns html version of a report.
    #     """
    #     if not data:
    #         data = {}
    #     data.setdefault('report_type', 'html')
    #     data = self._get_rendering_context(docids, data)

    #     #_logger.info("_render_qweb_html data : " + str(data))

    #     #_logger.info("_render_qweb_html data['docs'].create_date : " + str(data['docs'].x_employee_id.x_staff_id))

    #     _logger.info("_render_qweb_html type(data['docs'].x_employee_id.create_date) : " + str(type(data['docs'].x_employee_id.create_date)))

    #     if data['docs'].x_employee_id.x_staff_id:
    #         data['docs'].x_employee_id.x_staff_id = self._replace_eng_arabic(data['docs'].x_employee_id.x_staff_id)
        
    #     #data['docs'].x_employee_id.x_hiring_date = self._convert_arabic_dt(self._replace_eng_arabic(str(data['docs'].x_employee_id.x_hiring_date)))
        
    #     if data['docs'].x_employee_id.identification_id:
    #         data['docs'].x_employee_id.identification_id = self._replace_eng_arabic(data['docs'].x_employee_id.identification_id)
        
    #     if data['docs'].x_employee_id.phone:
    #         data['docs'].x_employee_id.phone = self._replace_eng_arabic(data['docs'].x_employee_id.phone)

    #     if data['docs'].x_employee_id.work_phone:
    #         data['docs'].x_employee_id.work_phone = self._replace_eng_arabic(data['docs'].x_employee_id.work_phone)

    #     if data['docs'].x_employee_id.mobile_phone:
    #         data['docs'].x_employee_id.mobile_phone = self._replace_eng_arabic(data['docs'].x_employee_id.mobile_phone)
        
    #     #data['docs'].x_employee_id.create_date = self._conver_date_arabic(str(data['docs'].x_employee_id.create_date))
        
    #     if data['docs'].x_employee_id.x_age:
    #         data['docs'].x_employee_id.x_age = self._replace_eng_arabic(str(data['docs'].x_employee_id.x_age))
        

    #     return self._render_template(self.sudo().report_name, data), 'html'


    
    def _replace_eng_arabic(self, text):

        text = text.replace("1","١")
        text = text.replace("2","٢")
        text = text.replace("3","٣")
        text = text.replace("4","٤")
        text = text.replace("5","٥")
        text = text.replace("6","٦")
        text = text.replace("7","٧")
        text = text.replace("8","٨")
        text = text.replace("9","٩")
        text = text.replace("0","٠")

        _logger.info("_replace_eng_arabic text : " + str(text))


        return text


    def _conver_date_arabic(self, _date):
        _logger.info("_conver_date_arabic _date : " + str(_date))
        _text_ar = self._replace_eng_arabic(str(_date))
        _logger.info("_conver_date_arabic _text_ar : " + str(_text_ar))

        _date_a = parser.parse(_text_ar)
        #_data_a = pd.to_datetime(_text_ar)
        # _date_b = _date_a.date()

        return _date_a



