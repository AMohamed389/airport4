from odoo import fields, models, api
from odoo.exceptions import UserError
import datetime

class JobBalancing(models.Model):
    _name = 'job_balancing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'supervision_position'
    employee_id = fields.Many2one('hr.employee', string='Employee')
    hr_job_id = fields.Many2one('hr.job', domain="[('x_is_supervision_job','=',True)]", string='Job Position')
    supervision_position = fields.Selection(
        [('رئيس قسم', 'رئيس قسم'), ('مدير عام', 'مدير عام'), ('رئيس قطاع', 'رئيس قطاع'),
         ('مستشار رئيس مجلس الإدارة', 'مستشار رئيس مجلس الإدارة'), ('مدير إدارة', 'مدير إدارة'),
         ('مساعد رئيس قطاع', 'مساعد رئيس قطاع'), ('رئيس ورش', 'رئيس ورش'), ('مدير منوب', 'مدير منوب'),
         ('مستشار قانونى', 'مستشار قانونى'),
         ('نائب مديرعام', 'نائب مديرعام'), ('مديرادارة', 'مديرادارة'), ('نائب ثان مديرعام', 'نائب ثان مديرعام'),
         ('نائب مديرعام', 'نائب مديرعام'), ('مساعد مديرعام', 'مساعد مديرعام'), ('مستشار', 'مستشار'),
         ('مستشار هندسى', 'مستشار هندسى'),
         ('مساعد رئيس مجلس الإدارة', 'مساعد رئيس مجلس الإدارة'), ('مشرف على إدارة', 'مشرف على إدارة'),
         ('مستشاررئيس مجلس الإدارة', 'مستشاررئيس مجلس الإدارة'),
         ('مستشار رئيس قطاع', 'مستشار رئيس قطاع')],string='Supervision Position')
    supervision_position_start_date = fields.Date(string='Job Position Start Date')
    decision_number = fields.Char(string='Decision Number', index=True, tracking=True)
    decision_date = fields.Date(string='Decision Date', index=True, tracking=True)
    attachments = fields.Binary(string='Attachment', index=True, tracking=True)
    x_sched_type = fields.Selection(related='employee_id.x_work_schedule_type')

    state = fields.Selection([
        ('draft', 'Draft'), ('submit', 'Submit'), ('completed', 'Completed')
    ], string='Run State', default='draft', index=True, tracking=True)

    def set_to_draft(self):
        if self.state == 'submit' or self.state == 'completed':
            self.state = 'draft'

    def submit_order(self):

        emp = self.env['hr.employee'].search([])
        for _rec in emp:
            if _rec.job_id == self.hr_job_id and _rec.job_id.x_is_supervision_job == True:
                raise UserError(f'{_rec.name},{_rec.x_staff_id} has this position')
        if self.state == 'draft':
            self.state = 'submit'

    def complete_order(self):
        if self.state == 'submit':
            self.state = 'completed'

        line = {
            'job_balancing_id': self.id,
            'supervision_position_start_date': self.supervision_position_start_date,
            'job_id': self.hr_job_id,
        }
        emp_supervision_job = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).write(line)



