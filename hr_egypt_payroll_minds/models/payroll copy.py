# -*- coding: utf-8 -*-

from re import T
from odoo import models, fields, api, _

from datetime import datetime
from datetime import date
from copy import deepcopy
from ast import literal_eval
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.tools.safe_eval import safe_eval
import base64

import logging
_logger = logging.getLogger(__name__)


class taxation(models.Model):
    _inherit = 'hr.payslip'

    ded_line_ids = fields.One2many('hr.payslip.line', 'slip_id', compute="_get_deductions", readonly=True)
    merit_line_ids = fields.One2many('hr.payslip.line', 'slip_id', compute="_get_merits", readonly=True)
    net_tax_line_ids = fields.One2many('hr.payslip.line', 'slip_id', compute="_get_net_tax", readonly=True)

    def _get_deductions(self):
        self.ded_line_ids = self.env['hr.payslip.line'].search(['|','|','|','|',
                                                                ('category_code', '=', 'TDED'),
                                                                ('category_code', '=', 'NTDED'),
                                                                ('category_code', '=', 'TS'),
                                                                ('category_code', '=', 'NTS'),
                                                                ('category_code','=','TOTALDED')
                                                                ,('slip_id','=',self.id)])

        return self.ded_line_ids

    def _get_merits(self):
        self.merit_line_ids = self.env['hr.payslip.line'].search(['|','|','|',
                                                                ('category_code', '=', 'TMRT'),
                                                                ('category_code', '=', 'NTMRT'),
                                                                ('category_code','=','GROSS'),
                                                                ('category_code','=','BASIC')
                                                                ,('slip_id','=',self.id)])
        return self.merit_line_ids

    def _get_net_tax(self):
        self.net_tax_line_ids = self.env['hr.payslip.line'].search(['|',('category_code', '=', 'TAX'),
                                                                ('category_code', '=', 'NET')
                                                                ,('slip_id','=',self.id)])
        return self.net_tax_line_ids

    def get_salary_m_taxes(self, emp_id, netgross):

        emp_rec = self.env['hr.contract'].search([('employee_id', '=', int(emp_id))])
        dt_start = emp_rec.date_start
        _logger.info('dt_start maged ! "%s"' % (str(dt_start)))

        today = date.today()
        _logger.info('today maged ! "%s"' % (str(today)))

        start_month = datetime.strptime(str(dt_start), "%Y-%m-%d").month
        _logger.info('start_month maged ! "%s"' % (str(start_month)))
        start_year = datetime.strptime(str(dt_start), "%Y-%m-%d").year
        _logger.info('start_year maged ! "%s"' % (str(start_year)))

        current_month = today.month
        _logger.info('current_month maged ! "%s"' % (str(current_month)))
        current_year = today.year
        _logger.info('current_year maged ! "%s"' % (str(current_year)))

        return -1 * self.EgyPayroll(emp_id, netgross)

    def sum_inputs_codes(self, payslip_id, code, contract_id):

        _logger.info('self.id maged ! "%s"' % (str(payslip_id)))
        _logger.info('code maged ! "%s"' % (str(code)))
        _logger.info('contract_id maged ! "%s"' % (str(contract_id)))

        inputs = self.env['hr.payslip.input'].search([('payslip_id','=',payslip_id)])
        _logger.info('inputs maged ! "%s"' % (str(inputs)))

        result = 0.0

        for input in inputs:
            if input[0]['code'] == code and int(input[0]['contract_id'])  == contract_id:
                result = result + input[0]['amount']

        _logger.info('result maged ! "%s"' % (str(result)))

        return result

    def SalaryTaxTo600Layer(self, emp_id, salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0

        personal_exempt = (1 / 12) * 9000
        if emp_id.x_has_disability_condition:
            personal_exempt = (1 / 12) * 13500

        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (15000 / 12):
            _logger.info('salary <= (15000 / 12) ==> maged !')
            tax0 = salary * 0
            _logger.info('tax0 = salary * 0 ==> maged ! "%s"' % (str(tax0)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
            _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('(0 / 12) <= salary_after_deduct_tax <= (15000 / 12) ==> maged 1 !')
                tax2_5 = salary_after_deduct_tax * 0.025
                _logger.info('tax2_5 = salary_after_deduct_tax * 0.025 ==> maged ! "%s"' % (str(tax2_5)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result
            else:
                tax2_5 = (15000/12) * 0.025
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax2_5 ==> maged ! "%s"' % (str(tax2_5)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))


            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('0 <= salary_after_deduct_tax <= (15000 / 12) ==> maged !')
                tax10= salary_after_deduct_tax * 0.1
                _logger.info('tax10 = salary_after_deduct_tax * 0.1 ==> maged ! "%s"' % (str(tax10)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result
            else:
                tax10 = (15000 / 12) * 0.1
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax10 ==> maged ! "%s"' % (str(tax10)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if 0 <= salary_after_deduct_tax <= (15000 / 12):
                    _logger.info('0 <= salary_after_deduct_tax <= (15000 / 12) ==> maged !')
                    tax15 = salary_after_deduct_tax * 0.15
                    _logger.info('tax15 = salary_after_deduct_tax * 0.15 ==> maged ! "%s"' % (str(tax15)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                        str(result)))
                    return result
                else:
                    tax15 = (15000 / 12) * 0.15
                    _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                    salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                    _logger.info('tax15 ==> maged ! "%s"' % (str(tax15)))
                    _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                    if 0 <= salary_after_deduct_tax <= (140000 / 12):
                        _logger.info('0 <= salary_after_deduct_tax <= (140000 / 12) ==> maged !')
                        tax20 = salary_after_deduct_tax * 0.2
                        _logger.info('tax20 = salary_after_deduct_tax * 0.20 ==> maged ! "%s"' % (str(tax20)))
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        _logger.info(
                            'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                str(result)))
                        return result
                    else:
                        tax20 = (140000 / 12) * 0.2
                        _logger.info('(140000 / 12) ==> maged ! "%s"' % (str((140000 / 12))))
                        salary_after_deduct_tax = salary_after_deduct_tax - (140000 / 12)
                        _logger.info('tax20 ==> maged ! "%s"' % (str(tax20)))
                        _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                        if 0 <= salary_after_deduct_tax <= (200000 / 12):
                            _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                            tax22_5 = salary_after_deduct_tax * 0.225
                            _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                            _logger.info(
                                'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                    str(result)))
                            return result
                        else:
                            tax22_5 = (200000 / 12) * 0.225
                            _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                            salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                            _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                            _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                            if salary_after_deduct_tax >= (200001 / 12):
                                _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                                tax25 = salary_after_deduct_tax * 0.25
                                _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                                _logger.info(
                                    'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                        str(result)))
                                return result
                            else:
                                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                                return result

    def SalaryTaxFrom601To700Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (30000 / 12):
            _logger.info('salary <= (30000 / 12) ==> maged !')
            tax2_5 = salary * 0.025
            _logger.info('tax2_5 = salary * 0.025 ==> maged ! "%s"' % (str(tax2_5)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            tax2_5 = (30000 / 12) * 0.025
            _logger.info('(30000 / 12) ==> maged ! "%s"' % (str((30000 / 12))))
            salary_after_deduct_tax = salary_after_deduct_tax - (30000 / 12)
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (30000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('(0 / 12) <= salary_after_deduct_tax <= (15000 / 12) ==> maged 1 !')
                tax10 = salary_after_deduct_tax * 0.1
                _logger.info('tax10 = salary_after_deduct_tax * 0.1 ==> maged ! "%s"' % (str(tax10)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info(
                    'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result
            else:
                tax10 = (15000 / 12) * 0.1
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax10 ==> maged ! "%s"' % (str(tax10)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if 0 <= salary_after_deduct_tax <= (15000 / 12):
                    _logger.info('0 <= salary_after_deduct_tax <= (15000 / 12) ==> maged !')
                    tax15 = salary_after_deduct_tax * 0.15
                    _logger.info('tax10 = salary_after_deduct_tax * 0.15 ==> maged ! "%s"' % (str(tax15)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                    return result
                else:
                    tax15 = (15000 / 12) * 0.15
                    _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                    salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                    _logger.info('tax15 ==> maged ! "%s"' % (str(tax15)))
                    _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))


                    if 0 <= salary_after_deduct_tax <= (140000 / 12):
                        _logger.info('0 <= salary_after_deduct_tax <= (140000 / 12) ==> maged !')
                        tax20 = salary_after_deduct_tax * 0.2
                        _logger.info('tax20 = salary_after_deduct_tax * 0.20 ==> maged ! "%s"' % (str(tax20)))
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                str(result)))
                        return result

                    else:

                        tax20 = (140000 / 12) * 0.2
                        _logger.info('(140000 / 12) ==> maged ! "%s"' % (str((140000 / 12))))
                        salary_after_deduct_tax = salary_after_deduct_tax - (140000 / 12)
                        _logger.info('tax20 ==> maged ! "%s"' % (str(tax20)))
                        _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                        if 0 <= salary_after_deduct_tax <= (200000 / 12):
                            _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                            tax22_5 = salary_after_deduct_tax * 0.225
                            _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                            return result

                        else:
                            tax22_5 = (200000 / 12) * 0.225
                            _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                            salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                            _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                            _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                            if salary_after_deduct_tax >= (200001 / 12):
                                _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                                tax25 = salary_after_deduct_tax * 0.25
                                _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                                _logger.info(
                                    'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                        str(result)))

                                return result
                            else:
                                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                                return result

    def SalaryTaxFrom701To800Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (45000 / 12):
            _logger.info('salary <= (45000 / 12) ==> maged !')
            tax10 = salary * 0.1
            _logger.info('tax10 = salary * 0.1 ==> maged ! "%s"' % (str(tax10)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            tax2_5 = (45000 / 12) * 0.1
            _logger.info('(45000 / 12) ==> maged ! "%s"' % (str((45000 / 12))))
            salary_after_deduct_tax = salary_after_deduct_tax - (45000 / 12)
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (30000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

            if 0 <= salary_after_deduct_tax <= (15000 / 12):
                _logger.info('(0 / 12) <= salary_after_deduct_tax <= (15000 / 12) ==> maged 1 !')
                tax15 = salary_after_deduct_tax * 0.15
                _logger.info('tax10 = salary_after_deduct_tax * 0.15 ==> maged ! "%s"' % (str(tax15)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
                return result

            else:
                tax15 = (15000 / 12) * 0.15
                _logger.info('(15000 / 12) ==> maged ! "%s"' % (str((15000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (15000 / 12)
                _logger.info('tax15 ==> maged ! "%s"' % (str(tax15)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if 0 <= salary_after_deduct_tax <= (140000 / 12):
                    _logger.info('0 <= salary_after_deduct_tax <= (140000 / 12) ==> maged !')
                    tax20 = salary_after_deduct_tax * 0.2
                    _logger.info('tax20 = salary_after_deduct_tax * 0.20 ==> maged ! "%s"' % (str(tax20)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                        str(result)))
                    return result

                else:

                    tax20 = (140000 / 12) * 0.2
                    _logger.info('(140000 / 12) ==> maged ! "%s"' % (str((140000 / 12))))
                    salary_after_deduct_tax = salary_after_deduct_tax - (140000 / 12)
                    _logger.info('tax20 ==> maged ! "%s"' % (str(tax20)))
                    _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                    if 0 <= salary_after_deduct_tax <= (200000 / 12):
                        _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                        tax22_5 = salary_after_deduct_tax * 0.225
                        _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        _logger.info(
                            'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                str(result)))
                        return result

                    else:
                        tax22_5 = (200000 / 12) * 0.225
                        _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                        salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                        _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                        _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                        if salary_after_deduct_tax >= (200001 / 12):
                            _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                            tax25 = salary_after_deduct_tax * 0.25
                            _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                            _logger.info(
                                'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                    str(result)))

                            return result
                        else:
                            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                            return result

    def SalaryTaxFrom801To900Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (60000 / 12):
            _logger.info('salary <= (60000 / 12) ==> maged !')
            tax15 = salary * 0.15
            _logger.info('tax15 = salary * 0.15 ==> maged ! "%s"' % (str(tax15)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            tax2_5 = (60000 / 12) * 0.15
            _logger.info('(60000 / 12) ==> maged ! "%s"' % (str((60000 / 12))))
            salary_after_deduct_tax = salary_after_deduct_tax - (60000 / 12)
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (30000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

            if 0 <= salary_after_deduct_tax <= (140000 / 12):
                _logger.info('0 <= salary_after_deduct_tax <= (140000 / 12) ==> maged !')
                tax20 = salary_after_deduct_tax * 0.2
                _logger.info('tax20 = salary_after_deduct_tax * 0.20 ==> maged ! "%s"' % (str(tax20)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                    str(result)))
                return result

            else:

                tax20 = (140000 / 12) * 0.2
                _logger.info('(140000 / 12) ==> maged ! "%s"' % (str((140000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (140000 / 12)
                _logger.info('tax20 ==> maged ! "%s"' % (str(tax20)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if 0 <= salary_after_deduct_tax <= (200000 / 12):
                    _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                    tax22_5 = salary_after_deduct_tax * 0.225
                    _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info(
                        'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                            str(result)))
                    return result

                else:
                    tax22_5 = (200000 / 12) * 0.225
                    _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                    salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                    _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                    _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                    if salary_after_deduct_tax >= (200001 / 12):
                        _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                        tax25 = salary_after_deduct_tax * 0.25
                        _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        _logger.info(
                            'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                                str(result)))

                        return result
                    else:
                        result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                        return result

    def SalaryTaxFrom901To1000Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (200000 / 12):
            _logger.info('salary <= (200000 / 12) ==> maged !')
            tax20 = salary * 0.2
            _logger.info('tax20 = salary * 0.2 ==> maged ! "%s"' % (str(tax20)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            tax20 = (200000 / 12) * 0.2
            _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
            salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))


            if 0 <= salary_after_deduct_tax <= (200000 / 12):
                _logger.info('0 <= salary_after_deduct_tax <= (200000 / 12) ==> maged !')
                tax22_5 = salary_after_deduct_tax * 0.225
                _logger.info('tax22_5 = salary_after_deduct_tax * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info(
                    'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                        str(result)))
                return result

            else:
                tax22_5 = (200000 / 12) * 0.225
                _logger.info('(200000 / 12) ==> maged ! "%s"' % (str((200000 / 12))))
                salary_after_deduct_tax = salary_after_deduct_tax - (200000 / 12)
                _logger.info('tax22_5 ==> maged ! "%s"' % (str(tax22_5)))
                _logger.info('salary_after_deduct_tax ==> maged ! "%s"' % (str(salary_after_deduct_tax)))

                if salary_after_deduct_tax >= (200001 / 12):
                    _logger.info('salary_after_deduct_tax >= (200001 / 12) ==> maged !')
                    tax25 = salary_after_deduct_tax * 0.25
                    _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    _logger.info(
                        'result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (
                            str(result)))

                    return result
                else:
                    result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                    return result

    def SalaryTaxFrom1001Layer(self,salary):

        tax0 = 0.0
        tax2_5 = 0.0
        tax10 = 0.0
        tax15 = 0.0
        tax20 = 0.0
        tax22_5 = 0.0
        tax25 = 0.0
        result = 0.0
        personal_exempt = (1 / 12) * 9000
        salary = salary - personal_exempt
        salary_after_deduct_tax = salary

        if salary <= (400000 / 12):
            _logger.info('salary <= (400000 / 12) ==> maged !')
            tax22_5 = salary * 0.225
            _logger.info('tax22_5 = salary * 0.225 ==> maged ! "%s"' % (str(tax22_5)))
            result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
            _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))
            return result

        else:
            tax20 = (400000 / 12) * 0.225
            _logger.info('(400000 / 12) ==> maged ! "%s"' % (str((400000 / 12))))
            salary_after_deduct_tax = salary_after_deduct_tax - (400000 / 12)
            _logger.info('salary_after_deduct_tax = salary_after_deduct_tax - (400000 / 12) ==> maged ! "%s"' % (str(salary_after_deduct_tax)))


            if salary_after_deduct_tax >= 0:
                _logger.info('salary_after_deduct_tax >= 0 ==> maged !')
                tax25 = salary_after_deduct_tax * 0.25
                _logger.info('tax25 = salary_after_deduct_tax * 0.25 ==> maged ! "%s"' % (str(tax25)))
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                _logger.info('result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25 ==> maged ! "%s"' % (str(result)))

                return result
            else:
                result = tax0 + tax2_5 + tax10 + tax15 + tax20 + tax22_5 + tax25
                return result

    def EgyPayroll(self, emp_id, netgross):

        salary = netgross

        result = 0.0

        # personal_exempt = (1 / 12) * 9000
        # salary = salary - personal_exempt
        annual_netgross_salary = 12 * salary

        if annual_netgross_salary < 0:
            return result
        elif 0 <= annual_netgross_salary <= 600000:
            result = taxation.SalaryTaxTo600Layer(self, emp_id, salary)
            return result
        elif 600001 <= annual_netgross_salary <= 700000:
            result = taxation.SalaryTaxFrom601To700Layer(self, salary)
            return result
        elif 700000 < annual_netgross_salary <= 800000:
            result = taxation.SalaryTaxFrom701To800Layer(self, salary)
            return result
        elif 800000 < annual_netgross_salary <= 900000:
            result = taxation.SalaryTaxFrom801To900Layer(self, salary)
            return result
        elif 900000 < annual_netgross_salary <= 1000000:
            result = taxation.SalaryTaxFrom901To1000Layer(self, salary)
            return result
        elif annual_netgross_salary > 1000000:
            result = taxation.SalaryTaxFrom1001Layer(self, salary)
            return result

    def get_basic_salary(self, emp_id=False):
        if not emp_id:
            return 0.0
        
        _emp_card_rec = self.env["employee_card"].search([('employee_id','=',emp_id.id)])
        if _emp_card_rec:
            return _emp_card_rec.basic_salary

        return 0.0

    def get_domain_list(self, domain=False):
        return literal_eval(domain) if domain else []

    def get_employee_merit(self, _allowance=False, emp_id=False, _basic_calc=0.0):
        if not emp_id or not _allowance:
            return False

        if (_allowance.start_date and _allowance.start_date > self.date_to) \
            or (_allowance.end_date and _allowance.end_date < self.date_from):
            return False

        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_allowance.domain) if _allowance.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',emp_id.id)]

        _amount =  _allowance.amount
        _percent =  _allowance.percentage
        _min_amount =  _allowance.min_amount
        _max_amount =  _allowance.max_amount
        _name = _allowance.name
        _code = _allowance.code
        _employee_card_date = _allowance.employee_card_date
        _dic = {
            'name':_name,
            'code':_code,
            'amount':0.0,
            'rate':0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',emp_id.id)]
        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search



        _emp_domain = emp_id.search(_emp_concat_domain)
        if not _emp_domain:
            return False

        _rate = 0
        _employee_start_date =  _allowance.start_date
        if _employee_start_date and _allowance.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30
        
        if _amount:
            _dic['amount'] = _amount
        
        if _percent:

            if _allowance.employee_card_salary:
                # _emp_card_rec = self.env["employee_card"].search([('employee_id','=',emp_id.id),
                #                                                   ('date','=',_employee_card_date)])

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _allowance.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res


        _employee_start_date =  _allowance.start_date
        _employee_end_date = False
        _pay_slip_domain_calc = {}
        _missed = 0
        if _employee_start_date and _allowance.is_retroactive:
            _employee_end_date = _allowance.end_date
            _pay_slip_domain_calc['employee_id'] = [('employee_id','=',emp_id.id)]
            _pay_slip_domain_calc['state'] = [('state','=','done')]
            _pay_slip_domain_calc['date_from'] = [('date_from','>=',_employee_start_date)]
            if _employee_end_date:
                _pay_slip_domain_calc['date_to'] = [('date_to','<=',_employee_end_date)]
            
            _pay_slip_domain = []
            for key, search in _pay_slip_domain_calc.items():
                _pay_slip_domain += search

            _recs = self.env['hr.payslip'].search(_pay_slip_domain)
            if len(_recs) > 0:
                for _rec in _recs:
                    _line_ids = _rec.line_ids.mapped('code')
                    if _allowance.code not in _line_ids:
                        _missed += 1
            else:
                _day = _employee_start_date.day
                _month = _employee_start_date.month
                _year = _employee_start_date.year

                # _num_days = (self.date_to - _employee_start_date).days
                _num_months = (self.date_to.year - _employee_start_date.year) * 12 + (self.date_to.month - _employee_start_date.month)
                _num_years = relativedelta(self.date_to, _employee_start_date).years

                if _allowance.monthly:
                    _missed = round(_num_months,0)
                elif _allowance.years:
                    _missed = round(_num_years,0)

        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=',emp_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _allowance.code in _line_ids:
                    if _allowance.monthly:
                        return False

        _rate = (1 - _rate) + _missed
        _dic['rate'] = _rate
        _dic['amount'] = _dic['amount'] * _rate
        return _dic

    def get_specific_employee_merit(self, _employee_allowance=False, _basic_calc=0.0):
        if not _employee_allowance :
            return False

        if _employee_allowance.is_run \
            or (_employee_allowance.start_date and _employee_allowance.start_date > self.date_to) \
            or (_employee_allowance.end_date and _employee_allowance.end_date < self.date_from) \
            or _employee_allowance.run_date :
            return False

        _allowance_id = _employee_allowance.allowance_id
        _employee_id = _employee_allowance.employee_id

        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_allowance_id.domain) if _allowance_id.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',_employee_id.id)]

        _amount =  False
        if _employee_allowance.amount and _employee_allowance.amount > 0:
            _amount = _employee_allowance.amount
        elif _allowance_id and _allowance_id.amount > 0:
            _amount =  _allowance_id.amount

        _percent =  _allowance_id.percentage

        _min_amount =  _allowance_id.min_amount
        _max_amount =  _allowance_id.max_amount
        _name = _allowance_id.name
        _code = _allowance_id.code
        _employee_card_date = _allowance_id.employee_card_date

        
        _dic = {
            'name': _name,
            'code': _code,
            'amount': 0.0,
            'rate': 0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',_employee_id.id)]
        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search



        _emp_domain = _employee_id.search(_emp_concat_domain)
        if not _emp_domain:
            return False

        _rate = 0.0
        _employee_start_date =  _employee_allowance.allowance_id.start_date
        if _employee_start_date and _employee_allowance.allowance_id.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30

        _employee_start_date =  _employee_allowance.start_date
        if _employee_start_date and _employee_allowance.allowance_id.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30

        if _amount:
                
            _dic['amount'] = _amount
            if _allowance_id.once:
                _employee_allowance.payslip_id = self.id
                # _employee_allowance.is_run = True
                # _employee_allowance.run_date = datetime.now().date()
            

        if _percent:

            if _allowance_id.employee_card_salary:

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _allowance_id.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res
            
            if _allowance_id.once:
                _employee_allowance.payslip_id = self.id
                # _employee_allowance.is_run = True
                # _employee_allowance.run_date = datetime.now().date()

        _employee_start_date =  _employee_allowance.allowance_id.start_date
        if _employee_allowance.start_date:
            _employee_start_date =  _employee_allowance.start_date
        _employee_end_date = False
        _pay_slip_domain_calc = {}
        _missed = 0
        if _employee_start_date and _allowance_id.is_retroactive:
            _employee_end_date = _allowance_id.end_date
            if _employee_allowance.end_date:
                _employee_end_date = _employee_allowance.end_date
            
            _pay_slip_domain_calc['employee_id'] = [('employee_id','=',_employee_allowance.employee_id.id)]
            _pay_slip_domain_calc['state'] = [('state','=','done')]
            _pay_slip_domain_calc['date_from'] = [('date_from','>=',_employee_start_date)]
            if _employee_end_date:
                _pay_slip_domain_calc['date_to'] = [('date_to','<=',_employee_end_date)]
            
            _pay_slip_domain = []
            for key, search in _pay_slip_domain_calc.items():
                _pay_slip_domain += search

            _recs = self.env['hr.payslip'].search(_pay_slip_domain)
            if len(_recs) > 0:
                for _rec in _recs:
                    _line_ids = _rec.line_ids.mapped('code')
                    if _allowance_id.code not in _line_ids:
                        _missed += 1
            else:
                _day = _employee_start_date.day
                _month = _employee_start_date.month
                _year = _employee_start_date.year

                # _num_days = (self.date_to - _employee_start_date).days
                _num_months = (self.date_to.year - _employee_start_date.year) * 12 + (self.date_to.month - _employee_start_date.month)
                _num_years = relativedelta(self.date_to, _employee_start_date).years

                if _allowance_id.monthly:
                    _missed = round(_num_months,0)
                elif _allowance_id.years:
                    _missed = round(_num_years,0)

        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=',_employee_allowance.employee_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _allowance_id.code in _line_ids:
                    if _allowance_id.monthly:
                        return False

        _rate = (1 - _rate) + _missed
        _dic['rate'] = _rate
        _dic['amount'] = _dic['amount'] * _rate
        return _dic

    def get_specific_employee_deduction(self, _employee_deduction=False, _basic_calc=0.0):
        if not _employee_deduction :
            return False

        if _employee_deduction.is_run or _employee_deduction.run_date:
            return False

        _deduction_id = _employee_deduction.deduction_id
        _employee_id = _employee_deduction.employee_id

        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_deduction_id.domain) if _deduction_id.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',_employee_id.id)]

        _amount =  False
        if _employee_deduction.amount and _employee_deduction.amount > 0:
            _amount = _employee_deduction.amount
        elif _deduction_id and _deduction_id.amount > 0:
            _amount =  _deduction_id.amount

        _percent =  _deduction_id.percentage

        _min_amount =  _deduction_id.min_amount
        _max_amount =  _deduction_id.max_amount
        _name = _deduction_id.name
        _code = _deduction_id.code
        _employee_card_date = _deduction_id.employee_card_date

        
        _dic = {
            'name':_name,
            'code':_code,
            'amount':0.0,
            'rate':0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',_employee_id.id)]
        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search



        _emp_domain = _employee_id.search(_emp_concat_domain)
        if not _emp_domain:
            return False

        
        if _amount:
            _dic['amount'] = _amount
            if _deduction_id.once:
                _employee_deduction.payslip_id = self.id
                # _employee_deduction.is_run = True
                # _employee_deduction.run_date = datetime.now().date()
            

        if _percent:

            if _deduction_id.employee_card_salary:

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _deduction_id.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res
            
            if _deduction_id.once:
                _employee_deduction.payslip_id = self.id
                # _employee_deduction.is_run = True
                # _employee_deduction.run_date = datetime.now().date()

        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=',_employee_deduction.employee_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _deduction_id.code in _line_ids:
                    if _deduction_id.monthly:
                        return False

        _rate = 1
        _dic['rate'] = _rate
        _dic['amount'] = -1 * _dic['amount'] * _rate
        return _dic

    def get_specific_employee_subscription(self, _employee_subscription=False, _basic_calc=0.0):
        if not _employee_subscription :
            return False

        if (_employee_subscription.start_date and _employee_subscription.start_date > self.date_to) \
            or (_employee_subscription.end_date and _employee_subscription.end_date < self.date_from):
            return False
        
        if (_employee_subscription.subscription_id.start_date and _employee_subscription.subscription_id.start_date > self.date_to) \
            or (_employee_subscription.subscription_id.end_date and _employee_subscription.subscription_id.end_date < self.date_from):
            return False

        _subscription_id = _employee_subscription.subscription_id
        _employee_id = _employee_subscription.employee_id

        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_subscription_id.domain) if _subscription_id.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',_employee_id.id)]

        _amount =  False
        if _employee_subscription.amount and _employee_subscription.amount > 0:
            _amount = _employee_subscription.amount
        elif _subscription_id and _subscription_id.amount > 0:
            _amount =  _subscription_id.amount

        _percent =  _subscription_id.percentage

        _min_amount =  _subscription_id.minimum_amount
        _max_amount =  _subscription_id.maximum_amount
        _name = _subscription_id.name
        _code = _subscription_id.code
        _employee_card_date = _subscription_id.employee_card_date

        
        _dic = {
            'name':_name,
            'code':_code,
            'amount':0.0,
            'rate':0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',_employee_id.id)]

        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search



        _emp_domain = _employee_id.search(_emp_concat_domain)
        if not _emp_domain:
            return False


        _rate = 0.0
        _employee_start_date =  _employee_subscription.subscription_id.start_date
        if _employee_start_date and _employee_subscription.subscription_id.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30

        _employee_start_date =  _employee_subscription.start_date
        if _employee_start_date and _employee_subscription.subscription_id.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30

        
        if _amount:
            _dic['amount'] = _amount
            

        if _percent:

            if _subscription_id.employee_card_salary:

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _subscription_id.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res
            

        _employee_start_date =  _subscription_id.start_date
        if _employee_subscription.start_date:
            _employee_start_date =  _employee_subscription.start_date
        _employee_end_date = False
        _pay_slip_domain_calc = {}
        _missed = 0
        if _employee_start_date and _subscription_id.is_retroactive:
            _employee_end_date = _subscription_id.end_date
            if _employee_subscription.end_date:
                _employee_end_date = _employee_subscription.end_date
            
            _pay_slip_domain_calc['employee_id'] = [('employee_id','=',_employee_subscription.employee_id.id)]
            _pay_slip_domain_calc['state'] = [('state','=','done')]
            _pay_slip_domain_calc['date_from'] = [('date_from','>=',_employee_start_date)]
            if _employee_end_date:
                _pay_slip_domain_calc['date_to'] = [('date_to','<=',_employee_end_date)]
            
            _pay_slip_domain = []
            for key, search in _pay_slip_domain_calc.items():
                _pay_slip_domain += search

            _recs = self.env['hr.payslip'].search(_pay_slip_domain)
            if len(_recs) > 0:
                for _rec in _recs:
                    _line_ids = _rec.line_ids.mapped('code')
                    if _subscription_id.code not in _line_ids:
                        _missed += 1
            else:
                _day = _employee_start_date.day
                _month = _employee_start_date.month
                _year = _employee_start_date.year

                # _num_days = (self.date_to - _employee_start_date).days
                _num_months = (self.date_to.year - _employee_start_date.year) * 12 + (self.date_to.month - _employee_start_date.month)
                _num_years = relativedelta(self.date_to, _employee_start_date).years

                if _subscription_id.monthly:
                    _missed = round(_num_months,0)
                elif _subscription_id.years:
                    _missed = round(_num_years,0)

        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=', _employee_subscription.employee_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _subscription_id.code in _line_ids:
                    if _subscription_id.monthly:
                        return False

        _rate = (1 - _rate) + _missed
        _dic['rate'] = _rate
        _dic['amount'] = -1 * _dic['amount'] * _rate
        return _dic

    def get_employee_subscription(self, _subscription=False, emp_id=False, _basic_calc=0.0):
        if not emp_id or not _subscription:
            return False

        if (_subscription.start_date and _subscription.start_date > self.date_to) \
            or (_subscription.end_date and _subscription.end_date < self.date_from):
            return False

        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_subscription.domain) if _subscription.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',emp_id.id)]

        _amount =  _subscription.amount
        _percent =  _subscription.percentage
        _min_amount =  _subscription.minimum_amount
        _max_amount =  _subscription.maximum_amount
        _name = _subscription.name
        _code = _subscription.code
        _employee_card_date = _subscription.employee_card_date
        _dic = {
            'name':_name,
            'code':_code,
            'amount':0.0,
            'rate':0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',emp_id.id)]
        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search

        _emp_domain = emp_id.search(_emp_concat_domain)
        if not _emp_domain:
            return _dic


        _rate = 0.0
        _employee_start_date =  _subscription.start_date
        if _employee_start_date and _subscription.is_partial:
            _today_date = date(_employee_start_date.year, _employee_start_date.month, 1)
            num_months = (_employee_start_date.year - _today_date.year) * 12 + (_employee_start_date.month - _today_date.month)
            if num_months >= 0 and num_months < 1:
                num_days = (_employee_start_date - _today_date).days
                _rate = num_days / 30

        
        if _amount:
            _dic['amount'] = _amount
        
        if _percent:

            if _subscription.employee_card_salary:
                # _emp_card_rec = self.env["employee_card"].search([('employee_id','=',emp_id.id),
                #                                                   ('date','=',_employee_card_date)])

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _subscription.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res

        _employee_start_date =  _subscription.start_date
        _employee_end_date = False
        _pay_slip_domain_calc = {}
        _missed = 0
        if _employee_start_date and _subscription.is_retroactive:
            _employee_end_date = _subscription.end_date
            _pay_slip_domain_calc['employee_id'] = [('employee_id','=',emp_id.id)]
            _pay_slip_domain_calc['state'] = [('state','=','done')]
            _pay_slip_domain_calc['date_from'] = [('date_from','>=',_employee_start_date)]
            if _employee_end_date:
                _pay_slip_domain_calc['date_to'] = [('date_to','<=',_employee_end_date)]
            
            _pay_slip_domain = []
            for key, search in _pay_slip_domain_calc.items():
                _pay_slip_domain += search

            _recs = self.env['hr.payslip'].search(_pay_slip_domain)
            if len(_recs) > 0:
                for _rec in _recs:
                    _line_ids = _rec.line_ids.mapped('code')
                    if _subscription.code not in _line_ids:
                        _missed += 1
            else:
                _day = _employee_start_date.day
                _month = _employee_start_date.month
                _year = _employee_start_date.year

                # _num_days = (self.date_to - _employee_start_date).days
                _num_months = (self.date_to.year - _employee_start_date.year) * 12 + (self.date_to.month - _employee_start_date.month)
                _num_years = relativedelta(self.date_to, _employee_start_date).years

                if _subscription.monthly:
                    _missed = round(_num_months,0)
                elif _subscription.years:
                    _missed = round(_num_years,0)
                

        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=',emp_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _subscription.code in _line_ids:
                    if _subscription.monthly:
                        return False


        _rate = (1 - _rate) + _missed
        _dic['rate'] = _rate
        _dic['amount'] = -1 * _dic['amount'] * (1 - _rate)
        return _dic

    def get_employee_deduction(self, _deduction=False, emp_id=False, _basic_calc=0.0):
        if not emp_id or not _deduction:
            return False

        
        _domain = []
        _concat_domain = {}
        _domain =  self.get_domain_list(_deduction.domain) if _deduction.domain  else [('active','=',True)]
        _concat_domain["db_domain"] = _domain
        _concat_domain["dummy_emp_id_domain"] = [('id','=',emp_id.id)]

        _amount =  _deduction.amount
        _percent =  _deduction.percentage
        _min_amount =  _deduction.min_amount
        _max_amount =  _deduction.max_amount
        _name = _deduction.name
        _code = _deduction.code
        _employee_card_date = _deduction.employee_card_date
        _dic = {
            'name':_name,
            'code':_code,
            'amount':0.0,
            'rate':0.0,
        }

        _employee_card_domain = {}
        _employee_card_domain['employee_id'] = [('employee_id','=',emp_id.id)]
        if _employee_card_date:
            _employee_card_domain['date'] = [('date','=',_employee_card_date)]
            _employee_card_domain['active'] = ['|',('active','=',True),('active','=',False)]
        
        _emp_card_domain = []
        for key, search in _employee_card_domain.items():
            _emp_card_domain += search

        _emp_concat_domain = []
        for key, search in _concat_domain.items():
            _emp_concat_domain += search

        _emp_domain = emp_id.search(_emp_concat_domain)
        if not _emp_domain:
            return _dic
        
        if _amount:
            _dic['amount'] = _amount
        
        if _percent:

            if _deduction.employee_card_salary:
                # _emp_card_rec = self.env["employee_card"].search([('employee_id','=',emp_id.id),
                #                                                   ('date','=',_employee_card_date)])

                _emp_card_rec = self.env["employee_card"].search(_emp_card_domain)

                if _emp_card_rec:
                    _res = _emp_card_rec.basic_salary * (_percent/100)
                    if _res < _min_amount:
                        _dic['amount'] = _min_amount
                    if _res > _max_amount:
                        _dic['amount'] = _max_amount
                    _dic['amount'] = _res

            elif _deduction.comprehensive_wage:
                _res = _basic_calc * (_percent/100)
                if _res < _min_amount:
                    _dic['amount'] = _min_amount
                if _res > _max_amount:
                    _dic['amount'] = _max_amount
                _dic['amount'] = _res

        
        _pay_slip_domain_calc = {}
        _pay_slip_domain_calc['employee_id'] = [('employee_id','=',emp_id.id)]
        _pay_slip_domain_calc['state'] = [('state','=','done')]
        _pay_slip_domain_calc['date_from'] = [('date_from','>=',self.date_from)]
        _pay_slip_domain_calc['date_to'] = [('date_to','<=',self.date_to)]
        
        _pay_slip_domain = []
        for key, search in _pay_slip_domain_calc.items():
            _pay_slip_domain += search

        _recs = self.env['hr.payslip'].search(_pay_slip_domain)
        if len(_recs) > 0:
            for _rec in _recs:
                _line_ids = _rec.line_ids.mapped('code')
                if _deduction.code in _line_ids:
                    if _deduction.monthly:
                        return False


        _dic['rate'] = 1
        _dic['amount'] = -1 * _dic['amount']
        return _dic

    # def compute_sheet(self):
    #     payslips = self.filtered(lambda slip: slip.state in ['draft', 'verify'])
    #     # delete old payslip lines
    #     payslips.line_ids.unlink()
    #     for payslip in payslips:
    #         number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
    #         lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
    #         payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today()})
    #     return True

    def compute_sheet(self):
        payslips = self.filtered(lambda slip: slip.state in ['draft', 'verify'])
        # delete old payslip lines
        payslips.line_ids.unlink()
        for payslip in payslips:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
            # _lines_for = deepcopy(lines)
            # for _line in _lines_for:
            #     if _line[2]['code'] == "DTALW":
            #         _copy = deepcopy(_line)
            #         lines.remove(_line)
            #         _merit_recs = self.env['allowance'].search([('all_employees','=',True),
            #                                                     ('type','=','allowance'),
            #                                                     ('is_taxable','=',True)], order="name DESC")
            #         for _merit_rec in _merit_recs:
            #             _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, lines[0][2]['amount'])
            #             _new_line = deepcopy(_copy)
            #             _new_line[2]['name'] = _res_dict['name']
            #             _new_line[2]['code'] = _res_dict['code']
            #             _new_line[2]['amount'] = _res_dict['amount']
            #             _new_line[2]['merit_id'] = _merit_rec.id
            #             lines.append(_new_line)

            #     elif _line[2]['code'] == "DNTALW":
            #         _copy = deepcopy(_line)
            #         lines.remove(_line)
            #         _merit_recs = self.env['allowance'].search([('all_employees','=',True),
            #                                                     ('type','=','allowance'),
            #                                                     ('is_taxable','=',False)], order="name DESC")
            #         for _merit_rec in _merit_recs:
            #             _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, lines[0][2]['amount'])
            #             _new_line = deepcopy(_copy)
            #             _new_line[2]['name'] = _res_dict['name']
            #             _new_line[2]['code'] = _res_dict['code']
            #             _new_line[2]['amount'] = _res_dict['amount']
            #             _new_line[2]['merit_id'] = _merit_rec.id
            #             lines.append(_new_line)
                
                # elif _line[2]['code'] == "DTINC":
                #     _copy = deepcopy(_line)
                #     lines.remove(_line)
                #     _merit_recs = self.env['allowance'].search([('all_employees','=',True),
                #                                                 ('type','=','incentive'),
                #                                                 ('is_taxable','=',True)], order="name DESC")
                #     for _merit_rec in _merit_recs:
                #         _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, lines[0][2]['amount'])
                #         _new_line = deepcopy(_copy)
                #         _new_line[2]['name'] = _res_dict['name']
                #         _new_line[2]['code'] = _res_dict['code']
                #         _new_line[2]['amount'] = _res_dict['amount']
                #         _new_line[2]['merit_id'] = _merit_rec.id
                #         lines.append(_new_line)
                
                # elif _line[2]['code'] == "DNTINC":
                #     _copy = deepcopy(_line)
                #     lines.remove(_line)
                #     _merit_recs = self.env['allowance'].search([('all_employees','=',True),
                #                                                 ('type','=','incentive'),
                #                                                 ('is_taxable','=',False)], order="name DESC")
                #     for _merit_rec in _merit_recs:
                #         _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, lines[0][2]['amount'])
                #         _new_line = deepcopy(_copy)
                #         _new_line[2]['name'] = _res_dict['name']
                #         _new_line[2]['code'] = _res_dict['code']
                #         _new_line[2]['amount'] = _res_dict['amount']
                #         _new_line[2]['merit_id'] = _merit_rec.id
                #         lines.append(_new_line)
                
            payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today()})
        return True

    def _get_payslip_lines(self):
        self.ensure_one()

        localdict = self.env.context.get('force_payslip_localdict', None)
        if localdict is None:
            localdict = self._get_localdict()

        rules_dict = localdict['rules'].dict
        result_rules_dict = localdict['result_rules'].dict

        blacklisted_rule_ids = self.env.context.get('prevent_payslip_computation_line_ids', [])

        result = {}

        for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
            if rule.id in blacklisted_rule_ids:
                continue
            localdict.update({
                'result': None,
                'result_qty': 1.0,
                'result_rate': 100})
            if rule._satisfy_condition(localdict):
                amount, qty, rate = rule._compute_rule(localdict)
                #check if there is already a rule computed with that code
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                #set/overwrite the amount computed for this rule in the localdict
                
                _domain = {}
                _domain_calc = []
                _rule_name = None
                _rule_code = None
                _rule_merit_id = None
                _rule_deduction_id = None
                _rule_subscription_id = None

                if rule.code == "DTALW":
                    _domain['type'] = [('type','=','allowance')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }
                    
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',True)]
                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    _domain['start_date'] = [('start_date','>=',datetime.now().date())]
                    _domain['end_date'] = [('end_date','<',datetime.now().date())]

                    
                    for key, search in _domain.items():
                        _domain_calc += search
                    
                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "allowance" and not _merit_rec.allowance_id.all_employees == False and _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }
                
                elif rule.code == "DNTALW":
                    _domain['type'] = [('type','=','allowance')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',False)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "allowance" and not _merit_rec.allowance_id.all_employees and not _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DTJINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]
                        elif _merit_rec.job_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTJINC"]["amount"]
                        elif _merit_rec.job_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTJINC"]["amount"]
                        elif _merit_rec.extra_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTEINC"]["amount"]
                        elif _merit_rec.extra_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTEINC"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }
                    
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',True)]
                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    _domain['start_date'] = [('start_date','>=',datetime.now().date())]
                    _domain['end_date'] = [('end_date','<',datetime.now().date())]

                    
                    for key, search in _domain.items():
                        _domain_calc += search
                    
                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees == False and _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTJINC"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTJINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTEINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTEINC"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }
                
                elif rule.code == "DNTJINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]
                        elif _merit_rec.job_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTJINC"]["amount"]
                        elif _merit_rec.job_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTJINC"]["amount"]
                        elif _merit_rec.extra_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTEINC"]["amount"]
                        elif _merit_rec.extra_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTEINC"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',False)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees and not _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTJINC"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTJINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTEINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTEINC"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DTEINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]
                        elif _merit_rec.job_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTJINC"]["amount"]
                        elif _merit_rec.job_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTJINC"]["amount"]
                        elif _merit_rec.extra_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTEINC"]["amount"]
                        elif _merit_rec.extra_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTEINC"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }
                    
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',True)]
                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    _domain['start_date'] = [('start_date','>=',datetime.now().date())]
                    _domain['end_date'] = [('end_date','<',datetime.now().date())]

                    
                    for key, search in _domain.items():
                        _domain_calc += search
                    
                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees == False and _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTJINC"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTJINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTEINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTEINC"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }
                
                elif rule.code == "DNTEINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]
                        elif _merit_rec.job_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTJINC"]["amount"]
                        elif _merit_rec.job_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTJINC"]["amount"]
                        elif _merit_rec.extra_incentive and _merit_rec.is_taxable:
                            _input_amount = result["DTEINC"]["amount"]
                        elif _merit_rec.extra_incentive and not _merit_rec.is_taxable:
                            _input_amount = result["DNTEINC"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['type'] = [('allowance_id.type','=','allowance')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',False)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees and not _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTJINC"]["amount"]
                            elif _merit_rec.allowance_id.job_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTJINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DTEINC"]["amount"]
                            elif _merit_rec.allowance_id.extra_incentive and not _merit_rec.allowance_id.is_taxable:
                                _input_amount = result["DNTEINC"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DTINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['type'] = [('allowance_id.type','=','incentive')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',True)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees and _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DNTINC":
                    _domain['type'] = [('type','=','incentive')]
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['allowance'].search(_domain_calc, order="name ASC")

                    for _merit_rec in _merit_recs:

                        _input_amount = 0.0
                        if _merit_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _merit_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_merit(_merit_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_merit_id = _merit_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['type'] = [('allowance_id.type','=','incentive')]
                    # _domain['all_employees'] = [('allowance_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('allowance_id.is_taxable','=',False)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    _domain['start_date'] = [('start_date','>=',datetime.now().date())]
                    _domain['end_date'] = [('end_date','<',datetime.now().date())]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _merit_recs = self.env['employee_allowance'].search(_domain_calc)

                    for _merit_rec in _merit_recs:
                        
                        if _merit_rec.allowance_id.type == "incentive" and not _merit_rec.allowance_id.all_employees and not _merit_rec.allowance_id.is_taxable:

                            _input_amount = 0.0
                            if _merit_rec.allowance_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _merit_rec.allowance_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_merit(_merit_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_merit_id = _merit_rec.allowance_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DTDED":
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    for key, search in _domain.items():
                        _domain_calc += search

                    _deduction_recs = self.env['deduction'].search(_domain_calc, order="name ASC")

                    for _deduction_rec in _deduction_recs:

                        _input_amount = 0.0
                        if _deduction_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _deduction_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_deduction(_deduction_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_deduction_id = _deduction_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }
                    

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['all_employees'] = [('deduction_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('deduction_id.is_taxable','=',True)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',datetime.now().date())]
                    # _domain['end_date'] = [('end_date','<',datetime.now().date())]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _deduction_recs = self.env['employee_deduction'].search(_domain_calc)

                    for _deduction_rec in _deduction_recs:
                        
                        if not _deduction_rec.deduction_id.all_employees and _deduction_rec.deduction_id.is_taxable:

                            _input_amount = 0.0
                            if _deduction_rec.deduction_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _deduction_rec.deduction_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_deduction(_deduction_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_deduction_id = _deduction_rec.deduction_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DNTDED":
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    for key, search in _domain.items():
                        _domain_calc += search

                    _deduction_recs = self.env['deduction'].search(_domain_calc, order="name ASC")

                    for _deduction_rec in _deduction_recs:

                        _input_amount = 0.0
                        if _deduction_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _deduction_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_deduction(_deduction_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_deduction_id = _deduction_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                            }

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_deduction_id = None
                    # _domain['all_employees'] = [('deduction_id.all_employees','=',False)]
                    # _domain['is_taxable'] = [('deduction_id.is_taxable','=',False)]
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    _domain['not_run'] = [('is_run','=',False)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _deduction_recs = self.env['employee_deduction'].search(_domain_calc)

                    for _deduction_rec in _deduction_recs:

                        if not _deduction_rec.deduction_id.all_employees and not _deduction_rec.deduction_id.is_taxable:

                            _input_amount = 0.0
                            if _deduction_rec.deduction_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _deduction_rec.deduction_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_deduction(_deduction_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_deduction_id = _deduction_rec.deduction_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                }

                elif rule.code == "DTS":
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',True)]

                    for key, search in _domain.items():
                        _domain_calc += search

                    _subscription_recs = self.env['subscription'].search(_domain_calc, order="name ASC")

                    for _subscription_rec in _subscription_recs:

                        _input_amount = 0.0
                        if _subscription_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _subscription_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_subscription(_subscription_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_subscription_id = _subscription_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                                'subscription_id': _rule_subscription_id,
                            }
                    

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_subscription_id = None
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _subscription_recs = self.env['employee_subscription'].search(_domain_calc)

                    for _subscription_rec in _subscription_recs:
                        
                        if not _subscription_rec.subscription_id.all_employees and _subscription_rec.subscription_id.is_taxable:

                            _input_amount = 0.0
                            if _subscription_rec.subscription_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _subscription_rec.subscription_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_subscription(_subscription_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_subscription_id = _subscription_rec.subscription_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                    'subscription_id': _rule_subscription_id,
                                }

                elif rule.code == "DNTS":
                    _domain['all_employees'] = [('all_employees','=',True)]
                    _domain['is_taxable'] = [('is_taxable','=',False)]

                    for key, search in _domain.items():
                        _domain_calc += search

                    _subscription_recs = self.env['subscription'].search(_domain_calc, order="name ASC")

                    for _subscription_rec in _subscription_recs:

                        _input_amount = 0.0
                        if _subscription_rec.employee_card_salary:
                            _input_amount = result["BASIC_EG"]["amount"]
                        elif _subscription_rec.comprehensive_wage:
                            _input_amount = result["GROSS_EG"]["amount"]

                        _res_dict = self.get_employee_subscription(_subscription_rec, self.employee_id, _input_amount)
                        if _res_dict:
                            _rule_name = _res_dict['name']
                            _rule_code = _res_dict['code']
                            # _rule_amount = _res_dict['amount']
                            _rule_subscription_id = _subscription_rec.id
                            amount = _res_dict['amount']
                            _rule_amount = _res_dict['amount']
                            qty = _res_dict['rate']
                            tot_rule = amount * qty * rate / 100.0
                            localdict[_rule_code] = tot_rule
                            result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                            rules_dict[_rule_code] = rule
                            # sum the amount for its salary category
                            localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                            result[_rule_code] = {
                                'sequence': rule.sequence,
                                'code': _rule_code,
                                'name': _rule_name,
                                'note': rule.note,
                                'salary_rule_id': rule.id,
                                'contract_id': localdict['contract'].id,
                                'employee_id': localdict['employee'].id,
                                'amount': _rule_amount,
                                'quantity': qty,
                                'rate': rate,
                                'slip_id': self.id,
                                'merit_id': _rule_merit_id,
                                'deduction_id': _rule_deduction_id,
                                'subscription_id': _rule_subscription_id,
                            }
                    

                    _domain = {}
                    _domain_calc = []
                    _rule_name = None
                    _rule_code = None
                    _rule_merit_id = None
                    _rule_subscription_id = None
                    _domain['employee'] = [('employee_id','=',self.employee_id.id)]
                    # _domain['start_date'] = [('start_date','>=',self.date_from)]
                    # _domain['end_date'] = ['|',('end_date','<',self.date_from),('end_date','=',None)]

                    
                    for key, search in _domain.items():
                        _domain_calc += search

                    _subscription_recs = self.env['employee_subscription'].search(_domain_calc)

                    for _subscription_rec in _subscription_recs:
                        
                        if not _subscription_rec.subscription_id.all_employees and not _subscription_rec.subscription_id.is_taxable:

                            _input_amount = 0.0
                            if _subscription_rec.subscription_id.employee_card_salary:
                                _input_amount = result["BASIC_EG"]["amount"]
                            elif _subscription_rec.subscription_id.comprehensive_wage:
                                _input_amount = result["GROSS_EG"]["amount"]

                            _res_dict = self.get_specific_employee_subscription(_subscription_rec, _input_amount)
                            if _res_dict:
                                _rule_name = _res_dict['name']
                                _rule_code = _res_dict['code']
                                # _rule_amount = _res_dict['amount']
                                _rule_subscription_id = _subscription_rec.subscription_id.id
                                amount = _res_dict['amount']
                                _rule_amount = _res_dict['amount']
                                qty = _res_dict['rate']
                                tot_rule = amount * qty * rate / 100.0
                                localdict[_rule_code] = tot_rule
                                result_rules_dict[_rule_code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                                rules_dict[_rule_code] = rule
                                # sum the amount for its salary category
                                localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)

                                result[_rule_code] = {
                                    'sequence': rule.sequence,
                                    'code': _rule_code,
                                    'name': _rule_name,
                                    'note': rule.note,
                                    'salary_rule_id': rule.id,
                                    'contract_id': localdict['contract'].id,
                                    'employee_id': localdict['employee'].id,
                                    'amount': _rule_amount,
                                    'quantity': qty,
                                    'rate': rate,
                                    'slip_id': self.id,
                                    'merit_id': _rule_merit_id,
                                    'deduction_id': _rule_deduction_id,
                                    'subscription_id': _rule_subscription_id,
                                }

                else:
                    # create/overwrite the rule in the temporary results
                    _rule_code = rule.code
                    # _rule_amount = amount
                    # _rule_merit_id = _merit_rec.id


                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    result_rules_dict[rule.code] = {'total': tot_rule, 'amount': amount, 'quantity': qty}
                    rules_dict[rule.code] = rule
                    # sum the amount for its salary category
                    localdict = rule.category_id._sum_salary_rule_category(localdict, tot_rule - previous_amount)
                    # Retrieve the line name in the employee's lang
                    employee_lang = self.employee_id.sudo().address_home_id.lang

                    # This actually has an impact, don't remove this line
                    context = {'lang': employee_lang}
                    if rule.code in ['BASIC', 'GROSS', 'NET']:  # Generated by default_get (no xmlid)
                        if rule.code == 'BASIC':
                            rule_name = _('Basic Salary')
                        elif rule.code == "GROSS":
                            rule_name = _('Gross')
                        elif rule.code == 'NET':
                            rule_name = _('Net Salary')

                        result[rule.code] = {
                            'sequence': rule.sequence,
                            'code': rule.code,
                            'name': rule_name,
                            'note': rule.note,
                            'salary_rule_id': rule.id,
                            'contract_id': localdict['contract'].id,
                            'employee_id': localdict['employee'].id,
                            'amount': amount,
                            'quantity': qty,
                            'rate': rate,
                            'slip_id': self.id,
                            'merit_id': _rule_merit_id,
                            'deduction_id': _rule_deduction_id,
                        }
                    else:
                        rule_name = rule.with_context(lang=employee_lang).name

                        result[rule.code] = {
                            'sequence': rule.sequence,
                            'code': rule.code,
                            'name': rule_name,
                            'note': rule.note,
                            'salary_rule_id': rule.id,
                            'contract_id': localdict['contract'].id,
                            'employee_id': localdict['employee'].id,
                            'amount': amount,
                            'quantity': qty,
                            'rate': rate,
                            'slip_id': self.id,
                            'merit_id': _rule_merit_id,
                            'deduction_id': _rule_deduction_id,
                            'subscription_id': _rule_subscription_id,
                        }
        return result.values()

    def _get_contract_wage(self):
        self.ensure_one()
        if self.employee_id:
            return self.get_basic_salary(self.employee_id)
        return 0.0

    def _compute_basic_net(self):
        for payslip in self:
            _basic_wage = payslip._get_salary_line_total('BASIC')
            _net_wage = payslip._get_salary_line_total('NET')

            payslip.basic_wage = _basic_wage
            payslip.net_wage = _net_wage

            _basic_wage_eg = payslip._get_salary_line_total('BASIC_EG')
            _net_wage_eg = payslip._get_salary_line_total('NET_EG')

            if _basic_wage_eg > _basic_wage:
                payslip.basic_wage = _basic_wage_eg
            
            if _net_wage_eg > _net_wage:
                payslip.net_wage = _net_wage_eg

    def action_payslip_done(self):
        if any(slip.state == 'cancel' for slip in self):
            raise ValidationError(_("You can't validate a cancelled payslip."))
        self.write({'state' : 'done'})
        self.mapped('payslip_run_id').action_close()

        _confirm_run_recs = self.env['employee_allowance'].search([('payslip_id','=',self.id),
                                                                   ('employee_id','=',self.employee_id.id)])
        for _rec in _confirm_run_recs:
            _line_ids = self.line_ids.mapped('code')
            if _rec.allowance_id.code in _line_ids:
                _rec.is_run = True
                _rec.run_date = datetime.now()
        
        _confirm_run_recs = self.env['employee_deduction'].search([('payslip_id','=',self.id),
                                                                    ('employee_id','=',self.employee_id.id)])
        for _rec in _confirm_run_recs:
            _line_ids = self.line_ids.mapped('code')
            if _rec.deduction_id.code in _line_ids:
                _rec.is_run = True
                _rec.run_date = datetime.now()
        

        # Validate work entries for regular payslips (exclude end of year bonus, ...)
        regular_payslips = self.filtered(lambda p: p.struct_id.type_id.default_struct_id == p.struct_id)
        for regular_payslip in regular_payslips:
            work_entries = self.env['hr.work.entry'].search([
                ('date_start', '<=', regular_payslip.date_to),
                ('date_stop', '>=', regular_payslip.date_from),
                ('employee_id', '=', regular_payslip.employee_id.id),
            ])
            work_entries.action_validate()

        if self.env.context.get('payslip_generate_pdf'):
            for payslip in self:
                if not payslip.struct_id or not payslip.struct_id.report_id:
                    report = self.env.ref('hr_payroll.action_report_payslip', False)
                else:
                    report = payslip.struct_id.report_id
                pdf_content, content_type = report.sudo()._render_qweb_pdf(payslip.id)
                if payslip.struct_id.report_id.print_report_name:
                    pdf_name = safe_eval(payslip.struct_id.report_id.print_report_name, {'object': payslip})
                else:
                    pdf_name = _("Payslip")
                # Sudo to allow payroll managers to create document.document without access to the
                # application
                attachment = self.env['ir.attachment'].sudo().create({
                    'name': pdf_name,
                    'type': 'binary',
                    'datas': base64.encodebytes(pdf_content),
                    'res_model': payslip._name,
                    'res_id': payslip.id
                })
                # Send email to employees
                subject = '%s, a new payslip is available for you' % (payslip.employee_id.name)
                template = self.env.ref('hr_payroll.mail_template_new_payslip', raise_if_not_found=False)
                if template:
                    email_values = {
                        'attachment_ids': attachment,
                    }
                    template.send_mail(
                        payslip.id,
                        email_values=email_values,
                        notif_layout='mail.mail_notification_light')

    