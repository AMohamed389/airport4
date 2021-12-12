# -*- coding: utf-8 -*-
""" Employee Destination """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class EmployeeDestination(models.Model):
    """ Employee Destination """
    _name = 'employee_destination'
    _description = 'Employee Destination'

    name = fields.Char(string="Employee Destination", index=True, tracking=True)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)
