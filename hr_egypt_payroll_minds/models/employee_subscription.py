# -*- coding: utf-8 -*-
""" Employee Subscription """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeSubscription(models.Model):
    """ Employee Subscription """
    _name = 'employee_subscription'
    _description = 'Employee Subscription'
    _order = 'id DESC'

    employee_id = fields.Many2one('hr.employee', index=True, string="Employee", tracking=True)
    subscription_id = fields.Many2one('subscription', index=True, string="Subscription", tracking=True)
    # employee_card_id = fields.Many2one('employee_card', string="Employee Card",tracking=True)
    # daily = fields.Boolean(string='Daily',index=True,tracking=True)
    # monthly = fields.Boolean(string='Monthly',index=True,tracking=True)
    # yearly = fields.Boolean(string='Yearly',index=True,tracking=True)
    start_date = fields.Date(string='Start Date',index=True,tracking=True)
    end_date = fields.Date(string='End Date',index=True,tracking=True)
    amount = fields.Monetary(string="Amount Of Money", tracking=True)
    active = fields.Boolean(string='Active', index=True, tracking=True, default=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id.id, tracking=True)

