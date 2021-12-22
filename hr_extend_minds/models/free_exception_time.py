from odoo import fields, models,api


class FreeExceptionTime(models.Model):
    _name = 'free_exception_time'
    _rec_name = 'employee_id'
    employee_id = fields.Many2one('hr.employee', string="Employee", index=True, tracking=True)
    decision_date = fields.Date(string="Decision Date")
    decision_number = fields.Integer(string='Decision Number', index=True, tracking=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    type = fields.Selection([('تفرغ رياضي فرق الشركة', 'تفرغ رياضي فرق الشركة'),
                             ('تفرغ رياضي خارجي خاص', 'تفرغ رياضي خارجي خاص'),
                             ('تفرغ ايام الامتحانات', 'تفرغ ايام الامتحانات'),
                             ('تفرغ للعمودة و شياخة البلد', 'تفرغ للعمودة و شياخة البلد'),
                             ('تفرغ منحة دراسية بالخارج', 'تفرغ منحة دراسية بالخارج'),
                             ('تفرغ منتديات شباب\رئاسي', 'تفرغ منتديات شباب\رئاسي')], string="Type of Exception",)
    destination = fields.Text(string="Destination")
    note = fields.Text(string="Note")

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('x_staff_id', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
