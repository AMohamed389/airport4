from odoo import fields, models, api


class Delegation(models.Model):
    _name = 'delegation'
    employee_id = fields.Many2one('hr.employee')
    type_of_delegation = fields.Selection([('Internal Delegation', 'Internal Delegation'),
                                           ('External Delegation', 'External Delegation')],
                                          string='Type of delegation')

    @api.depends('type_of_delegation')
    @api.onchange('type_of_delegation')
    def check_type(self):
        x_company = self.env['transfer_company_name'].search([('name', '=', 'شركة ميناء القاهرة الجوي')], limit=1)
        x_company_all = self.env['transfer_company_name'].search([('name', '!=', 'شركة ميناء القاهرة الجوي')])
        airport_domain = self.env['airports'].search([('name', '!=', 'شركة ميناء القاهرة الجوي')])

        if self.type_of_delegation == 'Internal Delegation':
            self.delegate_to = x_company.id
            return {
                'domain': {
                    'delegate_from': [('id', 'in', x_company_all.ids)],
                    'delegate_to': [('id', '=', x_company.id)],
                    'from_airport': [('id', 'in', airport_domain.ids)]
                },
            }
        else:
            self.delegate_from = x_company.id
            return {
                'domain': {
                    'delegate_to': [('id', 'in', x_company_all.ids)],
                    'delegate_from': [('id', '=', x_company.id)],
                    'to_airport': [('id', 'in', airport_domain.ids)],

                }
            }

    delegate_from = fields.Many2one('transfer_company_name', string='Delegate From', index=True, tracking=True)
    delegate_to = fields.Many2one('transfer_company_name', string='Delegate To', index=True, tracking=True)

    from_airport = fields.Many2one('airports', string='From Airport', index=True, tracking=True)
    to_airport = fields.Many2one('airports', string='To Airport', index=True, tracking=True)

    delegate_from_name = fields.Char(related='delegate_from.name', string='Delegate From Name', store=True)
    delegate_to_name = fields.Char(related='delegate_to.name', string='Delegate To Name', store=True)

    decision_date = fields.Date(string='Decision date')
    decision_number = fields.Char(string='Decision number')

    period = fields.Char(compute='compute_delegation', string='Delegation period')

    period_date_from = fields.Date(string='Period date from')
    period_date_to = fields.Date(string='Period date to')
    attachments = fields.Binary(string='Attachment')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submit'), ('completed', 'Completed')
    ], string='Run State', default='draft', index=True, tracking=True)

    def name_get(self):
        result = []
        for rec in self:
            new_name = f'{rec.employee_id.name}, {rec.type_of_delegation}'
            result.append((rec.id, new_name))
        return result

    def set_to_draft(self):
        if self.state == 'submit' or self.state == 'completed':
            self.state = 'draft'

    def submit_order(self):
        if self.state == 'draft':
            self.state = 'submit'

    @api.depends('period_date_from', 'period_date_to')
    def compute_delegation(self):
        for rec in self:
            if rec.period_date_to and rec.period_date_from:

                date_from_days = rec.period_date_from
                date_to_days = rec.period_date_to
                days_res = str(date_to_days - date_from_days)
                day_res = days_res.replace(', 0:00:00', '')

                # date_from_months = rec.period_date_from.year * 12 + (rec.period_date_from.month - 1)
                # date_to_months = rec.period_date_to.year * 12 + (rec.period_date_to.month - 1)
                _num_months = (rec.period_date_to.year - rec.period_date_from.year) * 12 + (rec.period_date_to.month - rec.period_date_from.month)
                # months_res = date_to_months - date_from_months
                rec.period = f'days({day_res}), months({_num_months})'
            else:
                rec.period = 0.0

    def complete_order(self):
        if self.state == 'submit':
            self.state = 'completed'

        line = {
            'x_employee_id': self.employee_id.id,
            'x_type': self.type_of_delegation,
            'x_source_company': self.employee_id.department_id.name,
            'x_sector': self.employee_id.x_sector_name,
            'x_public_administration': self.employee_id.x_public_administration_name,
            'x_administration': self.employee_id.x_administration_name,
            'x_department': self.employee_id.x_section_name,
            'x_qualitative_group': self.employee_id.x_qualitative_group_id.name,
            'x_degree': self.employee_id.x_job_degree_id.name,
            'name': self.employee_id.job_id.name,
            'x_date_from': self.period_date_from,
            'x_date_to': self.period_date_to,
        }
        history = self.env['job_history'].search([('x_employee_id.id', '=', self.employee_id.id)]).create(line)
