from odoo import models, fields


class Deduction(models.Model):
    _name = 'deduction'
    _order = 'id DESC'
    name = fields.Char(string="Deduction", index=True, tracking=True)
    code = fields.Char(string="Deduction code", index=True, tracking=True)
    slice = fields.Char(string="Slice", index=True, tracking=True)
    desc = fields.Char(string="Description", index=True, tracking=True)
    group = fields.Char(string="Group", index=True, tracking=True)
    amount = fields.Monetary(string="Amount of money", tracking=True)
    percentage = fields.Float(string="Percentage", tracking=True)
    min_amount = fields.Monetary(string="Minimum amount", tracking=True)
    max_amount = fields.Monetary(string="Maximum amount", tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    once = fields.Boolean(string='Once', index=True, tracking=True)
    monthly = fields.Boolean(string='Monthly', index=True, tracking=True)
    yearly = fields.Boolean(string='Yearly', index=True, tracking=True)
    all_employees = fields.Boolean(string="All employees", index=True, tracking=True)
    employee_card_salary = fields.Boolean(string="Employee card salary", index=True, tracking=True)
    employee_card_date = fields.Date(string="Employee card date", index=True, tracking=True)
    comprehensive_wage = fields.Boolean(string="Comprehensive wage", index=True, tracking=True)
    job_incentive = fields.Boolean(string="Job Incentive", index=True, tracking=True)
    extra_incentive = fields.Boolean(string="Extra Incentive", index=True, tracking=True)
    # is_partial = fields.Boolean(string="Is Partial", index=True, tracking=True)
    is_retroactive = fields.Boolean(string="Is Retroactive", index=True, tracking=True)
    is_taxable = fields.Boolean(string="Is Taxable", index=True, tracking=True)
    domain = fields.Char(string="Domain", index=True, tracking=True)
    active = fields.Boolean(string="Active", index=True, tracking=True, default=True)
    deduction_employee_ids = fields.One2many('employee_deduction', 'deduction_id', store=True)
