from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from calendar import isleap

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
    
    static_job_incentive = fields.Boolean(string="Static Job Incentive", index=True, tracking=True)
    static_extra_incentive = fields.Boolean(string="Static Extra Incentive", index=True, tracking=True)

    x_calc_degree_date_years = fields.Float(string="Degree Date In Years", compute="_get_degree_date_years")

    # @api.constrains('static_job_incentive')
    # def _check_static_job_incentive(self):
    #     for _rec in self:
    #         if not _rec.employee_job_incentive_id:
    #             raise ValidationError(_("Job incentive field slice is empty !."))

    # @api.constrains('static_extra_incentive')
    # def _check_static_extra_incentive(self):
    #     for _rec in self:
    #         if not _rec.employee_extra_incentive_id:
    #             raise ValidationError(_("Extra incentive field slice is empty !."))

    def write(self, vals):

        # if vals.get('static_job_incentive') or self.static_job_incentive:
        #     if not vals.get('employee_job_incentive_id') and not self.employee_job_incentive_id:
        #         raise ValidationError(_("Job incentive field slice is empty !."))

        # if vals.get('static_extra_incentive') or self.static_extra_incentive:
        #     if not vals.get('employee_extra_incentive_id') and not self.employee_extra_incentive_id:
        #         raise ValidationError(_("Extra incentive field slice is empty !."))

        res = super(HrPayrollExtend, self).write(vals)

        if self.static_job_incentive:
            if not self.employee_job_incentive_id:
                raise ValidationError(_("Job incentive field slice is empty !."))
        
        if self.static_extra_incentive:
            if not self.employee_extra_incentive_id:
                raise ValidationError(_("Extra incentive field slice is empty !."))

        return res

    def _get_degree_date_years(self):
        for _rec in self:
            _years = self.calculate_number_of_years(_rec.x_job_degree_date, datetime.now().date())
            _rec.x_calc_degree_date_years = _years
            return _rec.x_calc_degree_date_years

    def calculate_number_of_years(self, _start_date=False, _end_date=False):

        if not _start_date or not _end_date:
            return 0
        
        diffyears = _end_date.year - _start_date.year
        difference  = _end_date - _start_date.replace(_end_date.year)
        days_in_year = isleap(_end_date.year) and 366 or 365
        difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year

        return difference_in_years
