from odoo import models, fields, api
from odoo.exceptions import UserError


class Transfer(models.Model):
    _name = "transfer"
    _description = "internal and external transfers "

    employee_id = fields.Many2one('hr.employee', string='Name', index=True, tracking=True)
    type_of_transfer = fields.Selection(
        [('Internal Transfer', 'Internal Transfer'), ('External Transfer', 'External Transfer')],
        string='Type Of Transfer',
        index=True, tracking=True)

    transfer_from = fields.Many2one('hr.department', string='Transfer From Internal', index=True, tracking=True)
    transfer_to = fields.Many2one('hr.department', string='Transfer To Internal', index=True, tracking=True)

    transfer_from_external = fields.Many2one('airports', string='Transfer From External', index=True, tracking=True)
    transfer_to_external = fields.Many2one('airports', string='Transfer To External', index=True, tracking=True)

    transfer_from_name = fields.Char(related='transfer_from.name',  store=True, index=True, string='Transfer From Name')
    transfer_to_name = fields.Char(related='transfer_to.name', store=True, index=True, string='Transfer To Name')

    decision_number = fields.Char(string='Decision Number', index=True, tracking=True)
    decision_date = fields.Date(string='Decision Date', index=True, tracking=True)
    attachments = fields.Binary(string='Attachment', index=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submit'), ('completed', 'Completed')
    ], string='Run State', default='draft', index=True, tracking=True)
    notes = fields.Text(string='Notes')

    @api.depends('type_of_transfer', 'employee_id', 'transfer_from_external', 'transfer_to_external')
    @api.onchange('type_of_transfer', 'employee_id', 'transfer_from_external', 'transfer_to_external')
    def check_type(self):
        # get_employee_dept = self.env['hr.employee'].search(
        #     [('department_id.id', '=', self.employee_id.department_id.id)])

        if self.type_of_transfer == 'Internal Transfer':
            get_internal = self.env['hr.department'].search(
                ['|', ('x_type', '=', 'Department'), ('x_type', '=', 'Administration')])
            self.transfer_from = self.employee_id.department_id.id
            return {
                'domain': {
                    'transfer_to': ['&', ('id', 'in', get_internal.ids),
                                    # ('id', '!=', get_employee_dept.department_id.id)],
                                    ('id', '!=', self.transfer_from.id if self.transfer_from else self.employee_id.department_id.id)],
                    'transfer_from': ['&', ('id', 'in', get_internal.ids),
                                    ('id', '!=', self.transfer_to.id if self.transfer_to else 0),
                                    ('id', '=', self.employee_id.department_id.id if not self.transfer_to else get_internal.ids)]
                }
            }
        else:
            get_airports_all = self.env['airports'].search([])
            # get_airports = self.env['airports'].search([('name', '!=', 'شركة ميناء القاهرة الجوي')])
            # if self.transfer_from_external.name == 'شركة ميناء القاهرة الجوي':
            #     return {
            #         'domain': {
            #             'transfer_to_external': [('id', 'in', get_airports.ids)],
            #         }
            #     }
            # else:
            #     return {
            #         'domain': {
            #             'transfer_to_external': [('id', 'in', get_airports_all.ids)],
            #         }
            #     }
            return {
                    'domain': {
                        'transfer_from_external': ['&', ('id', 'in', get_airports_all.ids),
                                                        ('id','!=',self.transfer_to_external.id if self.transfer_to_external else 0)],
                        'transfer_to_external': ['&', ('id', 'in', get_airports_all.ids),
                                                        ('id','!=',self.transfer_from_external.id if self.transfer_from_external else 0)],
                    }
                }

    def name_get(self):
        result = []
        for rec in self:
            new_name = f'{rec.employee_id.name}, {rec.type_of_transfer}'
            result.append((rec.id, new_name))
        return result

    def set_to_draft(self):
        if self.state == 'submit' or self.state == 'completed':
            self.state = 'draft'

    def submit_order(self):
        if self.state == 'draft':
            self.state = 'submit'

    def complete_order(self):
        if self.state == 'submit':
            self.state = 'completed'

        external = ''
        internal = ''

        if self.type_of_transfer == 'Internal Transfer':
            internal = self.transfer_from.name
        else:
            external = self.transfer_from_external.name

        line = {
            'x_employee_id': self.employee_id.id,
            'x_type': self.type_of_transfer,
            'x_source_company': internal if internal else external,
            'x_sector': self.employee_id.x_sector_name,
            'x_public_administration': self.employee_id.x_public_administration_name,
            'x_administration': self.employee_id.x_administration_name,
            'x_department': self.employee_id.x_section_name,
            'x_qualitative_group': self.employee_id.x_qualitative_group_id.name,
            'x_degree': self.employee_id.x_job_degree_id.name,
            'name': self.employee_id.job_id.name,
        }
        history = self.env['job_history'].search([('x_employee_id.id', '=', self.employee_id.id)]).create(line)
