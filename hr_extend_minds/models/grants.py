# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class Grants(models.Model):
    """ Grants """
    _name = 'grants'
    _description = 'Grants'
    _order = 'id DESC'

    hr_employee_id = fields.Many2one('hr.employee',string='Employee Name',index=True,tracking=True)
    grant_type_id = fields.Many2one('grant_type',index=True,tracking=True)
    grants_terms_id = fields.Many2one('grants_terms',index=True,tracking=True)
    diagnosis_id = fields.Many2one('employee_diagnosis_type',sting="Diagnosis Type",index=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount',index=True,tracking=True)
    document_date = fields.Date(string='Document Date',index=True,tracking=True)
    submission_date = fields.Date(string='submission Date',index=True,tracking=True)
    attachment = fields.Binary(string="Attachment")



