# from odoo import fields, models, api
#
#
# class ManagementDecision(models.Model):
#     _name = 'management_decision'
#
#     employee_id = fields.Many2one('hr.employee', string='Employee')
#     based_on = fields.Char(string='Based On')
#     done = fields.Char(string='What Is Done')
#     transfered_from = fields.Many2one('transfer')
#     transfered_to = fields.Many2one('transfer')
#     decision_number =