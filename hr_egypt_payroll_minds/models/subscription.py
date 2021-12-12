# -*- coding: utf-8 -*-
""" Subscription """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class Subscription(models.Model):
    """ Subscription """
    _name = 'subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id DESC'

    name = fields.Char(string="Name", tracking=True, index=True)
    code = fields.Char(string="Code", index=True, tracking=True)
    slice = fields.Char(string="Slice", index=True, tracking=True)
    desc = fields.Char(string="Description", index=True, tracking=True)
    group = fields.Char(string="Group", index=True, tracking=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id.id, tracking=True)
    start_date = fields.Date(string='Start Date', index=True, tracking=True)
    end_date = fields.Date(string='End Date', index=True, tracking=True)
    amount = fields.Monetary(string="Amount Of Money", currency_field='currency_id', tracking=True, index=True)
    percentage = fields.Float(string="Percentage", tracking=True, index=True)
    minimum_amount = fields.Monetary(string="Minimum Amount", currency_field='currency_id', tracking=True)
    maximum_amount = fields.Monetary(string="Maximum Amount", currency_field='currency_id', tracking=True)
    all_employees = fields.Boolean(string="All Employees", tracking=True, index=True)
    employee_card_salary = fields.Boolean(string="Card Salary", tracking=True, index=True)
    employee_card_date = fields.Date(string="Employee Card Date", index=True, tracking=True)
    comprehensive_wage = fields.Boolean(string="Comperhensive Wage", tracking=True, index=True)
    job_incentive = fields.Boolean(string="Job Incentive", index=True, tracking=True)
    extra_incentive = fields.Boolean(string="Extra Incentive", index=True, tracking=True)
    is_taxable = fields.Boolean(string="Is Taxable", tracking=True, index=True)
    is_partial = fields.Boolean(string="Is Partial", index=True, tracking=True)
    is_retroactive = fields.Boolean(string="Is Retroactive", index=True, tracking=True)
    domain = fields.Char(string="Domain", tracking=True)
    active = fields.Boolean(string="Active", tracking=True, index=True, default=True)
    monthly = fields.Boolean(string="Monthly", tracking=True, index=True)
    yearly = fields.Boolean(string="Yearly", tracking=True,index=True)
    employee_subscription_ids = fields.One2many('employee_subscription', 'subscription_id', tracking=True, string="Employee Subscriptions")



