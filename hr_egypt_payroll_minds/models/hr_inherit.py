from odoo import models, fields


class HrPayrollExtend(models.Model):
    _inherit = 'hr.employee'

    employee_allowance_ids = fields.One2many('employee_allowance', 'employee_id', store=True, index=True)
    employee_deduction_ids = fields.One2many('employee_deduction', 'employee_id', store=True, index=True)
    employee_subscription_ids = fields.One2many('employee_subscription', 'employee_id', store=True, index=True)
    x_type_designation = fields.Selection([('Permanent', 'Permanent'), ('Decade', 'Decade'),
                                           ('Pay for work', 'Pay for work'), ('Seconded from the company abroad', 'Seconded from the company abroad'),
                                           ('Delegated from abroad for the company', 'Delegated from abroad for the company'),
                                           ('On loan from the company abroad', 'On loan from the company abroad'),
                                           ('On loan to the company', 'On loan to the company'), ('Third parties', 'Third parties')],
                                          string='Designation Type',
                                          index=True, required=True, tracking=True)								  
    is_military = fields.Boolean(string="Is Military", index=True, tracking=True)
    is_exchange_representative = fields.Boolean(string="Is Exchange Representative", index=True, tracking=True)
    is_aircraft_fees = fields.Boolean(string="Is Aircraft Fees", index=True, tracking=True)
    is_car_fees = fields.Boolean(string="Is Car Fees", index=True, tracking=True)


