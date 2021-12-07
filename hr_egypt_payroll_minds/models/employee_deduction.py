from odoo import models, fields


class EmployeeDeduction(models.Model):
    _name = 'employee_deduction'
    _order = 'id DESC'

    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, tracking=True)
    deduction_id = fields.Many2one('deduction', string='Deduction', index=True, tracking=True)
    amount = fields.Monetary(string="Amount Of Money", tracking=True)
    # employee_card_id = fields.Many2one('employee_card', string='employee_card', index=True, tracking=True)
    payslip_id = fields.Many2one('hr.payslip', string='Payslip', index=True, tracking=True)
    # once = fields.Boolean(string='once', index=True, tracking=True)
    # monthly = fields.Boolean(string='monthly', index=True, tracking=True)
    # yearly = fields.Boolean(string='yearly', index=True, tracking=True)
    run_date = fields.Datetime(string='Run Date', index=True, tracking=True)
    is_run = fields.Boolean(string='Is Run', index=True, tracking=True)
    # start_date = fields.Datetime(string='start date', index=True, tracking=True)
    # end_date = fields.Datetime(string='end date', index=True, tracking=True)
    # used_date = fields.Datetime(string='used date', index=True, tracking=True)
    active = fields.Boolean(string="Active", index=True, tracking=True, default=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
