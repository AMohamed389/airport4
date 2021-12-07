# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date

import logging

_logger = logging.getLogger(__name__)


class job_hierarchy(models.Model):
    _name = 'job_hierarchy'
    _description = 'Job Hierarchy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id DESC'

    name = fields.Char(string="Name", index=True, tracking=True)
    attachment_store = fields.Binary(string="Attachment", tracking=True)
    file_name = fields.Char(string="File Name", index=True)
    attachment_doc = fields.Binary(string="Document", store=True, compute="_get_save_att")
    attachment_id = fields.Many2one('ir.attachment', index=True, tracking=True)

    @api.depends('attachment_store')
    def _get_save_att(self):
        for _rec in self:
            if _rec.attachment_store:
                _attachment = self.env['ir.attachment'].create({
                    'datas': _rec.attachment_store,
                    'name': _rec.file_name,
                    # 'mimetype': _rec.attachment_store.content_type,
                    # 'res_model': 'documents.document',
                    # 'res_id': 0,
                })

                _rec.attachment_id = _attachment.id

                _job_structure_folder_id = self.env.ref("hr_extend_minds.documents_folder_2")
                if _job_structure_folder_id:
                    _document_a = self.env['documents.document'].create({
                        'folder_id': _job_structure_folder_id.id,
                        'name': _rec.file_name,
                        'attachment_id': _attachment.id,
                    })

                    _attachment.write({
                        'res_model': 'documents.document',
                        'res_id': _document_a.id,
                    })



    def unlink(self):
        for _rec in self:
            if _rec.attachment_id:
                _attachment_doc_rec = self.env['documents.document'].search([
                                                        ('attachment_id','=',_rec.attachment_id.id),
                                                        ('name','=',_rec.file_name)]
                                                        , limit=1)
                
                #_logger.info("job_hierarchy unlink _rec : " + str(_rec))

                for __rec in _attachment_doc_rec:
                    __rec.unlink()
                
                
                _rec.attachment_id.unlink()
        
        result = super(job_hierarchy, self).unlink()
        return result



    _sql_constraints = [('constrain_name', 'UNIQUE (name)', 'The name is already exists !.')]
