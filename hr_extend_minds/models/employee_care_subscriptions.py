# -*- coding: utf-8 -*-
""" Employee Care Subscriptions """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeCareSubscriptions(models.Model):
    """ Employee Care Subscriptions """
    _name = 'employee_care_subscriptions'
    _description = 'Employee Care Subscriptions'

    hr_employee_id = fields.Many2one('hr.employee',string='Employee Name',index=True,tracking=True)
    care_subscriptions_type_id = fields.Many2one('care_subscriptions_type',string="Subscriptions Type",index=True,tracking=True)
    employee_destination_id = fields.Many2one('employee_destination',string="Destination",index=True,tracking=True)
    no_of_months = fields.Integer(string="No.of Months",index=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount',index=True,tracking=True)
    start_date = fields.Date(index=True,tracking=True)
    end_date = fields.Date(index=True,tracking=True)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)
