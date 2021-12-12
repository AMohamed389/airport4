# -*- coding: utf-8 -*-
""" Employee Service Name """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeServiceName(models.Model):
    """ Employee Service Name """
    _name = 'employee_service_name'
    _description = 'Employee Service Name'
    _order = 'id DESC'

    name = fields.Char(string="Service Name", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
