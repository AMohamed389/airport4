# -*- coding: utf-8 -*-
""" Service Provider """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class ServiceProvider(models.Model):
    """ Service Provider """
    _name = 'service_provider'
    _description = 'Service Provider'
    _order = 'id DESC'

    name = fields.Char(string="Service Provider Name", index=True, tracking=True)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)
