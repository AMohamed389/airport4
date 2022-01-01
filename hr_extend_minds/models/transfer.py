from odoo import models, fields, api
from odoo.exceptions import UserError


class Transfer(models.Model):
    _name = "transfer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "internal and external transfers "

    employee_id = fields.Many2one('hr.employee', string='Name', index=True, tracking=True)
    type_of_transfer = fields.Selection(
        [('Internal Transfer', 'Internal'), ('External Transfer', 'External')],
        string='Type Of Transfer',
        index=True, tracking=True)

    transfer_from = fields.Many2one('hr.department', string='Transfer From Internal', index=True, tracking=True)
    transfer_to = fields.Many2one('hr.department', string='Transfer To Internal', index=True, tracking=True)

    transfer_from_name = fields.Char(related='transfer_from.name', store=True, index=True, string='Transfer From Name')
    transfer_to_name = fields.Char(related='transfer_to.name', store=True, index=True, string='Transfer To Name')

    transfer_from_external = fields.Many2one('transfer_company_name', string='Transfer From External', index=True,
                                             tracking=True)
    transfer_to_external = fields.Many2one('transfer_company_name', string='Transfer To External', index=True,
                                           tracking=True)

    transfer_from_external_name = fields.Char(related='transfer_from_external.name', store=True, index=True)
    transfer_to_external_name = fields.Char(related='transfer_to_external.name', store=True, index=True)

    from_airport = fields.Many2one('transfer_company_name', string='From Airport', index=True, tracking=True)
    to_airport = fields.Many2one('transfer_company_name', string='To Airport', index=True, tracking=True)

    type_of_external_transfer = fields.Selection(
        [('Internal Transfer CAC', 'To CAC'), ('External Transfer CAC', 'From CAC')],
        string='Type Of External Transfer',
        index=True, tracking=True)

    @api.onchange('type_of_external_transfer')
    @api.depends('type_of_external_transfer')
    def check_t(self):
        x_company = self.env['transfer_company_name'].search([('name', 'not like', 'مطار ')])
        x_airport = self.env['transfer_company_name'].search([('name', 'ilike', 'مطار ')])
        if self.type_of_external_transfer == 'Internal Transfer CAC':
            self.transfer_from_external = False
            self.transfer_to_external = False
            self.from_airport = False
            self.to_airport = False
            return {
                'domain': {
                    'transfer_to_external': [('name', '=', 'شركة ميناء القاهرة الجوي')],
                    'transfer_from_external': ['&', ('id', 'in', x_company.ids),
                                               ('name', '!=', 'شركة ميناء القاهرة الجوي')],
                    'from_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.to_airport.id)],
                    'to_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.from_airport.id)]
                }
            }
        else:
            self.transfer_to_external = False
            self.transfer_from_external = False
            self.from_airport = False
            self.to_airport = False
            return {
                'domain': {
                    'transfer_from_external': [('name', '=', 'شركة ميناء القاهرة الجوي')],
                    'transfer_to_external': ['&', ('id', 'in', x_company.ids),
                                             ('name', '!=', 'شركة ميناء القاهرة الجوي')],
                    'from_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.to_airport.id)],
                    'to_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.from_airport.id)]
                }
            }

    decision_number = fields.Char(string='Decision Number', index=True, tracking=True)
    decision_date = fields.Date(string='Decision Date', index=True, tracking=True)
    attachments = fields.Binary(string='Attachment', index=True, tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submit'), ('completed', 'Completed')
    ], string='Run State', default='draft', index=True, tracking=True)
    notes = fields.Text(string='Notes')

    @api.depends('type_of_transfer', 'employee_id')
    @api.onchange('type_of_transfer', 'employee_id')
    def check_type(self):
        get_employee_dept = self.env['hr.employee'].search(
            [('department_id.id', '=', self.employee_id.department_id.id)])

        if self.type_of_transfer == 'Internal Transfer':
            get_internal = self.env['hr.department'].search([])
                # ['|', '|', '|', ('x_type', '=', 'Department'), ('x_type', '=', 'Administration'),
                #  ('x_type', '=', 'Public Administration'), ('x_type', '=', 'Sector')])
            self.transfer_from = get_employee_dept.department_id
            return {
                'domain': {
                    'transfer_to': ['&', ('id', 'in', get_internal.ids),
                                    ('id', '!=', get_employee_dept.department_id.id)],
                    'transfer_from': [('id', '=', get_employee_dept.department_id.id)]
                }
            }
        else:
            self.transfer_from = False
            self.transfer_to = False

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

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('x_staff_id', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
