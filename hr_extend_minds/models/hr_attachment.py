# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date
import mimetypes
import sys
import logging

_logger = logging.getLogger(__name__)


class hr_attachment(models.Model):
    _name = 'hr_attachment'
    _description = 'HR Attachments'
    _order = 'id DESC'

    name = fields.Char(string="File Name", index=True, tracking=True)
    x_datas = fields.Binary(string="File", attachment=True)
    # x_file_size = fields.Integer(string="File Size", store=True)
    # x_mime_type = fields.Char(string="Mime Type", default='application/octet-stream')
    x_res_model = fields.Char(string="Resource Model", index=True, store=True)
    x_res_id = fields.Integer(string="Resource ID", index=True, store=True)
    # x_res_name = fields.Char(string="Resource Name", index=True, store=True)
    x_notes = fields.Text(string="Notes", tracking=True, store=True)
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)


    @api.model   
    def create(self, vals):
        _logger.info(str("committee_employee create vals : ") + str(vals))

        # vals['x_mime_type'] = mimetypes.guess_type(vals['x_datas'])
        # vals['x_file_size'] = sys.getsizeof(vals['x_datas'])

        result = super(hr_attachment, self).create(vals)

        return result