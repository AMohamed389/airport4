from odoo import models, fields


class Allowance(models.Model):
    _name = 'allowance'
    _order = 'id DESC'

    name = fields.Char(string="Allowance Name", index=True, tracking=True)
    code = fields.Char(string="Allowance Code", index=True, tracking=True)
    type = fields.Selection([('allowance', 'Allowance'), ('incentive', 'Incentive'), ('slice', 'Slice')], 
                                    string="Type", index=True, tracking=True)
    start_date = fields.Date(string='Start Date', index=True, tracking=True)
    end_date = fields.Date(string='End Date', index=True, tracking=True)
    amount = fields.Monetary(string="Amount Of Money", tracking=True)
    percentage = fields.Float(string="Percentage", tracking=True)
    once = fields.Boolean(string='Once', index=True, tracking=True)
    monthly = fields.Boolean(string='Monthly', index=True, tracking=True)
    yearly = fields.Boolean(string='Yearly', index=True, tracking=True)
    min_amount = fields.Monetary(string="Minimum amount", tracking=True)
    max_amount = fields.Monetary(string="Maximum amount", tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    all_employees = fields.Boolean(string="All Employees", index=True, tracking=True)
    employee_card_salary = fields.Boolean(string="Employee Card Salary", index=True, tracking=True)
    employee_card_date = fields.Date(string="Employee Card Date", index=True, tracking=True)
    comprehensive_wage = fields.Boolean(string="Comprehensive Wage", index=True, tracking=True)
    is_taxable = fields.Boolean(string="Is Taxable", index=True, tracking=True)
    is_partial = fields.Boolean(string="Is Partial", index=True, tracking=True)
    is_retroactive = fields.Boolean(string="Is Retroactive", index=True, tracking=True)
    domain = fields.Char(string="Domain", index=True, tracking=True)
    active = fields.Boolean(string="Active", index=True, tracking=True, default=True)
    allowance_employee_ids = fields.One2many('employee_allowance', 'allowance_id', store=True, string="Allowance Employees")



    
