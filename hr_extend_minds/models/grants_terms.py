# -*- coding: utf-8 -*-
""" Grants Terms """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class GrantsTerms(models.Model):
    """ Grants Terms """
    _name = 'grants_terms'
    _description = 'Grants Terms'
    _order = 'id DESC'

    name = fields.Char(string="Grants Terms", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
