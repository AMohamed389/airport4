# -*- coding: utf-8 -*-
""" Employee Diagnosis """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeDiagnosisType(models.Model):
    """ Employee Diagnosis Type """
    _name = 'employee_diagnosis_type'
    _description = 'Employee Diagnosis Type'

    name = fields.Char(string="Diagnosis Type", index=True, tracking=True)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)


