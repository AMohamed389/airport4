# -*- coding: utf-8 -*-
""" Care Subscriptions Type """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError


class CareSubscriptionsType(models.Model):
    """ Care Subscriptions Type """
    _name = 'care_subscriptions_type'
    _description = 'Care Subscriptions Type'
    _order = 'id DESC'

    name = fields.Char(string="Subscription Type", index=True, tracking=True)
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)
