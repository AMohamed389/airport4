from odoo import fields, models, api


class TransferCompanyName(models.Model):
    _name = 'transfer_company_name'
    name = fields.Char(string='Company name')
    active = fields.Boolean(default=True)

