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


class committee_employee(models.Model):
    _name = 'committee_employee'
    _description = 'Committee Employees'
    _order = 'id DESC'

    #name = fields.Char(string="Decision Number", index=True, required=True, tracking=True)
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True,
                                     tracking=True, index=True)
    x_amount = fields.Monetary(string='Amount',index=True, required=True,tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True, tracking=True, index=True, default=lambda self: self.env.user.company_id.currency_id.id)
    # x_datas = fields.Binary(related="x_attachment.x_datas", string="File")
    #x_attachments = fields.One2many('documents.document', 'attachment_id', compute="_get_attachments", string="Attachments", ondelete="cascade")
    # x_datas = fields.Binary(string="File")
    x_attachments = fields.One2many('documents.document', string="Attachments", compute="_get_attachments")
    x_notes = fields.Text(string="Notes", tracking=True, store=True)
    x_committee_id = fields.Many2one('committee', string="Committee", index=True, tracking=True)
    
    x_document_folder_id = fields.Many2one('documents.folder', string="Document Folder", readonly=True, index=True, tracking=True, ondelete="cascade")
    
    active = fields.Boolean(string='Active', index=True, default=True, tracking=True)


    def unlink(self):
        # "your code"

        _doc_folder_rec= False

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

        result = super(committee_employee, self).unlink()

        return result


    @api.onchange('name')
    def onchange_name(self):

        if self.name:
            return {'domain': {
                'x_document_folder_id': [('name', '=', self.name),('parent_folder_id','=',self.x_committee_id.id)]
            }}


    @api.model   
    def create(self, vals):
        _logger.info(str("committee create vals : ") + str(vals))

        _employee_rec = self.env['hr.employee'].browse(int(vals['x_employee_id']))
        _committee_rec = self.env['committee'].browse(int(vals['x_committee_id']))
        if _committee_rec and _employee_rec:
            _committee_doc_folder_rec = self.env['documents.folder'].browse(_committee_rec.x_document_folder_id.id)
            
            if _committee_doc_folder_rec:
                _doc_folder_rec = self.env['documents.folder'].search([('name','=',_employee_rec.name),('parent_folder_id','=',_committee_doc_folder_rec.id)], limit=1)

                if not _doc_folder_rec and _committee_doc_folder_rec:
                    _doc_folder_create_rec = self.env['documents.folder'].create({
                        'name': _employee_rec.name,
                        'parent_folder_id': _committee_doc_folder_rec[0].id
                    })

                    vals['x_document_folder_id'] = int(_doc_folder_create_rec)
                
                else:
                    vals['x_document_folder_id'] = _doc_folder_rec[0].id

        

        result = super(committee_employee, self).create(vals)

        _logger.info(str("committee create result : ") + str(result))

        return result

    
    def _get_attachments(self):

        for _rec in self:
            _doc_list = self.env['documents.document'].search([('folder_id','=',_rec.x_document_folder_id.id)])
            if _doc_list:
                _rec.x_attachments = _doc_list
            else:
                _rec.x_attachments = None


    _sql_constraints = [('constrainname', 'UNIQUE (x_employee_id, x_committee_id)', 'Employee must be unique under the committee !.')]