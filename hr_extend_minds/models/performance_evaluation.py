from odoo import fields, models, api


class PerformanceEvaluation(models.Model):
    _name = 'performance_evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, tracking=True)
    evaluation = fields.Selection(
        [('ممتاز', 'ممتاز'), ('جيد جدا', 'جيد جدا'), ('جيد', 'جيد'), ('متوسط', 'متوسط'), ('ضعيف', 'ضعيف')],
        index=True, tracking=True, string='Evaluation')
    reason = fields.Char(string='Reason')
    score = fields.Char(string='Score')
    note = fields.Text(string='Note')
    personal_committee_no = fields.Char(string='Personal Committee Number')

    def select_year(self):
        year = 1990
        year_list = []
        for i in range(0, 60):
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    evaluation_year = fields.Selection(select_year, string="Evaluation Year", index=True, tracking=True)
    date = fields.Date(string='Evaluation Date', index=True, tracking=True)
