# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class GrantType(models.Model):
    """ Grant Type """
    _name = 'grant_type'
    _description = 'Grant Type'
    _order = 'id DESC'

    name = fields.Char(string="Grant Type", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, tracking=True)
