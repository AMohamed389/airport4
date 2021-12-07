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


class committee(models.Model):
    _name = 'committee'
    _description = 'Committeee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id DESC'

    name = fields.Char(string="Decision Number", index=True, required=True, tracking=True)

    x_date_from = fields.Date(string="Date From", index=True, tracking=True)
    x_date_to = fields.Date(string="Date To", index=True, tracking=True)
    # x_attachments = fields.One2many('hr_attachment', 'x_res_id', string="Attachments", store=True, index=True)
    # x_attachments = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'committee')], string="Attachments", store=True, index=True)
    # x_attachments = fields.One2many('documents.document', 'attachment_id', domain=[('res_model', '=', 'committee')], string="Attachments", store=True, index=True)
    #x_attachments = fields.One2many('documents.document', 'attachment_id', string="Attachments", compute="_get_attachments", ondelete="cascade")
    x_attachments = fields.One2many('documents.document', string="Attachments", compute="_get_attachments")
    x_notes = fields.Text(string="Notes", tracking=True, store=True)
    x_committee_employee = fields.One2many('committee_employee', 'x_committee_id', index=True, store=True)
    x_document_folder_id = fields.Many2one('documents.folder', string="Document Folder", readonly=True, index=True, tracking=True, ondelete="cascade")
    active = fields.Boolean(string='Active',index=True,default=True,tracking=True)


    def unlink(self):
        # "your code"

        self.x_committee_employee.unlink()

        _doc_folder_rec= None

        for _rec in self:
            _doc_folder_rec = self.env['documents.folder'].browse(_rec.x_document_folder_id.id)

        if _doc_folder_rec:
            _logger.info("committee_employee unlink _doc_folder_rec : " + str(_doc_folder_rec))

            _documents_share_recs = self.env['documents.share'].search([('folder_id','=',_doc_folder_rec.id)])
            _documents_document_recs = self.env['documents.document'].search([('folder_id','=',_doc_folder_rec.id)])

            for ___rec in _documents_share_recs:
                ___rec.sudo().unlink()
                    
            for ___rec in _documents_document_recs:
                ___rec.sudo().unlink()

            _doc_folder_rec.sudo().document_ids.unlink()
            _doc_folder_rec.sudo().unlink()

        result = super(committee, self).unlink()

        return result

    @api.onchange('name')
    def onchange_name(self):

        if self.name:
            return {'domain': {
                'x_document_folder_id': [('name', '=', self.name)]
            }}


    @api.model   
    def create(self, vals):
        _logger.info(str("committee create vals : ") + str(vals))

        _committee_doc_folder_rec = self.env.ref("hr_extend_minds.documents_folder_1")
        # _committee_doc_folder_rec = self.env['documents.folder'].search([('name','=','Committee')], limit=1)

        # if not _committee_doc_folder_rec:
        #     _committee_doc_folder_rec = self.env['documents.folder'].search([('name','=','لجنة')], limit=1)

        # if not _committee_doc_folder_rec:
        #     _committee_doc_folder_rec = self.env['documents.folder'].search([('name','=','اللجنة')], limit=1)
        
        # if not _committee_doc_folder_rec:
        #     _committee_doc_folder_rec = self.env['documents.folder'].search([('name','=','اللجان')], limit=1)

        _doc_folder_rec = self.env['documents.folder'].search([('name','=',vals['name'])], limit=1)

        if not _doc_folder_rec and _committee_doc_folder_rec:
            _doc_folder_create_rec = self.env['documents.folder'].create({
                'name': vals['name'],
                'parent_folder_id': _committee_doc_folder_rec.id,
                # 'parent_folder_id': _committee_doc_folder_rec[0].id
            })

            vals['x_document_folder_id'] = int(_doc_folder_create_rec)
        
        else:
            vals['x_document_folder_id'] = _doc_folder_rec[0].id

        
        result = super(committee, self).create(vals)

        _logger.info(str("committee create result : ") + str(result))

        return result

    
    def _get_attachments(self):

        for _rec in self:
            _doc_list = self.env['documents.document'].search([('folder_id','=',_rec.x_document_folder_id.id)])
            _rec.x_attachments = _doc_list


    