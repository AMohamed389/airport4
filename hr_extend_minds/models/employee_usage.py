# -*- coding: utf-8 -*-
""" Employee Usage """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeUsage(models.Model):
    """ Employee Usage """
    _name = 'employee_usage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_service_name_id'
    _description = 'Employee Usage'

    hr_employee_id = fields.Many2one('hr.employee', string='Employee Name',
                                     index=True, tracking=True)
    service_date = fields.Date(index=True, tracking=True)
    employee_service_name_id = fields.Many2one('employee_service_name',
                                               index=True, tracking=True)
    insurance_company = fields.Selection(
        [('1', 'Egypt Air Insurance'), ('2', 'DMS Insurance'),
         ('3', 'Gov Medical Insurance')], string='Insurance Company',
        index=True)
    medical_number = fields.Char(tracking=True, index=True,compute='_compute_medical_number', store=True)
    employee_diagnosis_type_id = fields.Many2one('employee_diagnosis_type',
                                                 sting="Diagnosis Type",
                                                 index=True, tracking=True)
    service_provider_id = fields.Many2one('service_provider',
                                          sting="Service Provider Name",
                                          index=True, tracking=True)
    service_group_id = fields.Many2one('service_group',
                                       sting="Service Group Name", index=True,
                                       tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True,
                                  tracking=True, index=True, default=lambda
            self: self.env.user.company_id.currency_id.id)
    service_fees = fields.Monetary(string='Service Fees', index=True,
                                   tracking=True)
    total_fees = fields.Monetary(string='Total Fees', index=True, tracking=True)
    discount = fields.Float(string='Discount (%)', digits='Discount',
                            default=0.0)
    after_discount = fields.Monetary(string='After Discount', index=True,
                                     tracking=True)
    after_bearing = fields.Monetary(string='After Bearing', index=True,
                                    tracking=True)
    deductions = fields.Monetary(string='Deductions', index=True, tracking=True)
    total = fields.Monetary(string='Total', index=True, tracking=True)
    notes = fields.Text(tracking=True)
    attachment = fields.Binary()

    @api.depends('insurance_company','hr_employee_id')
    def _compute_medical_number(self):
        """ Compute medical_number value """
        for rec in self:
            if rec.insurance_company:
                if rec.hr_employee_id:
                    if rec.insurance_company == '1':
                        rec.medical_number = rec.hr_employee_id.egypt_air_insurance
                    if rec.insurance_company == '2':
                        rec.medical_number = rec.hr_employee_id.dms_insurance
                    if rec.insurance_company == '3':
                        rec.medical_number = rec.hr_employee_id.gov_medical_insurance
