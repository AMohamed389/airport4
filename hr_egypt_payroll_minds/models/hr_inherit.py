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

    
    employee_group_id = fields.Many2one('employee_group', tracking=True, index=True, string="Employee Group")
    employee_group_child_id = fields.Many2one('employee_group_child', domain=lambda self: "[('employee_group_id','=',employee_group_id)]", tracking=True, index=True, string="Employee Group Child")
    
    employee_group_name = fields.Char(related='employee_group_id.name', string="Employee Group Name")
    employee_group_child_name = fields.Char(related='employee_group_child_id.name', string="Employee Group Child Name")

    employee_job_incentive_id = fields.Many2one('incentive_band', string="Job Incentive", domain="[('type','=','حافز وظيفي')]", tracking=True, index=True)
    employee_job_incentive_name = fields.Char(related="employee_job_incentive_id.name", string="Job Incentive Name")
    employee_job_incentive_code = fields.Char(related="employee_job_incentive_id.code", string="Job Incentive Code")
    
    employee_extra_incentive_id = fields.Many2one('incentive_band', string="Extra Incentive", domain="[('type','=','حافز اضافي')]", tracking=True, index=True)
    employee_extra_incentive_name = fields.Char(related="employee_extra_incentive_id.name", string="Extra Incentive Name")
    employee_extra_incentive_code = fields.Char(related="employee_extra_incentive_id.code", string="Extra Incentive Code")
    