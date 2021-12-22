from odoo import fields, models, api


class Loan(models.Model):
    _name = 'loan'
    _rec_name = 'employee_id'
    employee_id = fields.Many2one('hr.employee')
    type_of_loan = fields.Selection([('Internal','Internal Loan'),('External','External Loan')])

    @api.onchange('type_of_loan')
    def check_type(self):
        x_company = self.env['transfer_company_name'].search([('name', 'not like', 'مطار ')])
        x_airport = self.env['transfer_company_name'].search([('name', 'ilike', 'مطار ')])
        if self.type_of_loan == 'Internal':
            self.loan_from = False
            self.loan_to = False
            return {
                    'domain':{
                        'loan_to': [('name', '=', 'شركة ميناء القاهرة الجوي')],
                        'loan_from': ['&', ('id', 'in', x_company.ids), ('name', '!=', 'شركة ميناء القاهرة الجوي')],
                        'from_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.to_airport.id)],
                        'to_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.from_airport.id)]
                    }
                }
        else:
            self.loan_to = False
            self.loan_from = False

            return {
                    'domain': {
                        'loan_from': [('name', '=', 'شركة ميناء القاهرة الجوي')],
                        'loan_to': ['&', ('id', 'in', x_company.ids), ('name', '!=', 'شركة ميناء القاهرة الجوي')],
                        'from_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.to_airport.id)],
                        'to_airport': ['&', ('id', 'in', x_airport.ids), ('id', '!=', self.from_airport.id)]
                    }
                }

    loan_from = fields.Many2one('transfer_company_name', string='Loan From', index=True, tracking=True)
    loan_to = fields.Many2one('transfer_company_name', string='Loan To', index=True, tracking=True)

    from_airport = fields.Many2one('transfer_company_name', string='From Airport', index=True, tracking=True)
    to_airport = fields.Many2one('transfer_company_name', string='To Airport', index=True, tracking=True)
    loan_from_name = fields.Char(related='loan_from.name', string='Loan From Name', store=True)
    loan_to_name = fields.Char(related='loan_to.name', string='Loan To Name', store=True)

    decision_date = fields.Date(string='Decision date')
    decision_number = fields.Char(string='Decision number')

    period = fields.Char(string='Loan period', compute='compute_loan_period')
    period_date_from = fields.Date(string='Period date from')
    period_date_to = fields.Date(string='Period date to')
    attachments = fields.Binary(string='Attachment')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submit'), ('completed', 'Completed')
    ], string='Run State', default='draft', index=True, tracking=True)

    def set_to_draft(self):
        if self.state == 'submit' or self.state == 'completed':
            self.state = 'draft'

    def submit_order(self):
        if self.state == 'draft':
            self.state = 'submit'

    @api.depends('period_date_from', 'period_date_to')
    def compute_loan_period(self):
        for rec in self:
            if rec.period_date_to and rec.period_date_from:

                date_from_days = rec.period_date_from
                date_to_days = rec.period_date_to
                days_res = str(date_to_days - date_from_days)
                day_res = days_res.replace(', 0:00:00', '')

                date_from_months = rec.period_date_from.year * 12 + (rec.period_date_from.month - 1)
                date_to_months = rec.period_date_to.year * 12 + (rec.period_date_to.month - 1)

                months_res = date_to_months - date_from_months
                rec.period = f'days({day_res}), months({months_res})'
            else:
                rec.period = 0.0

    def complete_order(self):
        if self.state == 'submit':
            self.state = 'completed'

        internal_source = ''
        external_source = ''
        if self.type_of_loan == 'Internal':
            internal_source = self.loan_to_name
        else:
            external_source = self.loan_from_name

        line = {
            'x_employee_id': self.employee_id.id,
            'x_type': self.type_of_loan,
            'x_source_company': internal_source if internal_source else external_source,
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
