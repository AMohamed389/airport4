from odoo import models, fields


class EmployeeAllowance(models.Model):
    _name = 'employee_allowance'
    _order = 'id DESC'

    employee_id = fields.Many2one('hr.employee', string='employee', index=True, tracking=True)
    allowance_id = fields.Many2one('allowance', string='allowance', index=True, tracking=True)
    amount = fields.Monetary(string="Amount Of Money", tracking=True)
    # employee_card_id = fields.Many2one('employee_card', string='employee_card', index=True, tracking=True)
    payslip_id = fields.Many2one('hr.payslip', string='payslip', index=True, tracking=True)
    # once = fields.Boolean(string='once', index=True, tracking=True)
    # monthly = fields.Boolean(string='monthly', index=True, tracking=True)
    # yearly = fields.Boolean(string='yearly', index=True, tracking=True)
    start_date = fields.Date(string='Start Date', index=True, tracking=True)
    end_date = fields.Date(string='End Date', index=True, tracking=True)
    is_run = fields.Boolean(string='is run', index=True, tracking=True)
    run_date = fields.Datetime(string='run date', index=True, tracking=True)
    active = fields.Boolean(string="active", index=True, tracking=True, default=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
