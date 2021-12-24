from odoo import fields, models, api
from odoo.exceptions import UserError

class SessionCommittee(models.Model):
    _name = 'committee_session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'committee_session_id'
    session_date = fields.Date(string='Session Date')
    allowance_percentage = fields.Selection(related='employee_session_id.allowance_percentage',
                                            string="Allowance Percentage")
    allowance_amount = fields.Float(compute="calc_amount", string="Allowance Amount")
    note = fields.Text(string="Note")
    employee_session_id = fields.Many2many('committee_employee', string='Employees Session', store=True)
    committee_session_id = fields.Many2one('committee', string='Committee')
    employee_id = fields.Many2one('hr.employee')

    @api.onchange('committee_session_id')
    def get_committee_session_id_employee(self):
        for _rec in self:
            return {
                    'domain': {
                        'employee_session_id': [('id', 'in', _rec.committee_session_id.x_committee_employee.ids)],
                    }
                }

    @api.depends('allowance_percentage')
    def calc_amount(self):
        for _rec in self:
            emp_allowance_amount = _rec.env['committee_employee'].search([('id', 'in', _rec.employee_session_id.ids)])
            total = sum(emp_allowance_amount.mapped('x_amount')) * float(_rec.allowance_percentage) / 100
            _rec.allowance_amount = total
