# -*- coding: utf-8 -*-
""" Service Provider """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class ServiceProvider(models.Model):
    """ Service Provider """
    _name = 'service_group'
    _description = 'Service Group'
    _order = 'id DESC'

    name = fields.Char(string="Service Group Name", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)