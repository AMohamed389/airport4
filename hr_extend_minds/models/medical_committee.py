# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class MedicalCommittee(models.Model):
    """ Medical Committee """
    _name = 'medical_committee'
    _description = 'Medical Committee'
    _order = 'id DESC'

    hr_employee_id = fields.Many2one('hr.employee',string='Employee Name',index=True,tracking=True)
    date = fields.Date(index=True,tracking=True)
    diagnosis_id = fields.Many2one('employee_diagnosis_type',sting="Diagnosis",index=True, required=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount',index=True,tracking=True)
    destination_number = fields.Integer(index=True,tracking=True)
    destination_date = fields.Date(index=True,tracking=True)
    attachment = fields.Binary(string="Attachment")

