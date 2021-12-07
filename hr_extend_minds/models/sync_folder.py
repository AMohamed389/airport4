# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date


import logging
_logger = logging.getLogger(__name__)


class sync_folder (models.Model):
    _name = 'sync_folder'
    _description = 'Sync Folders'
    _order = "id DESC"

    state = fields.Selection([
        ('Draft', 'Draft'),('Completed', 'Completed')
    ], string='Report State' ,default='Draft', index=True, tracking=True)

    
    def sync_employees_folder(self):

        # _doc_folder_rec = self.env['documents.folder'].search([('name','=','الموارد البشرية')], limit=1)

        # if not _doc_folder_rec:
        #     _doc_folder_rec = self.env['documents.folder'].search([('name','=','HR')], limit=1)

        _doc_folder_rec = self.env.ref('documents_hr.documents_hr_folder')

        if not _doc_folder_rec:
            return False
        
        for _rec in _doc_folder_rec:
            
            #_logger.info("sync_folder sync_employees_folder _rec : " + str(_rec))
            _child_folder = self.env['documents.folder'].search([('parent_folder_id','=',_doc_folder_rec.id)])

            for __rec in _child_folder:
                
                _employee_recs = self.env['hr.employee'].search([('x_document_folder_id','=',__rec.id)])
                _documents_share_recs = self.env['documents.share'].search([('folder_id','=',__rec.id)])

                if not _employee_recs:

                    for ___rec in _documents_share_recs:
                        ___rec.sudo().unlink()
                    
                    _documents_document_recs = self.env['documents.document'].search([('folder_id','=',__rec.id)])
                    for ___rec in _documents_document_recs:
                        ___rec.sudo().unlink()

                    __rec.sudo().document_ids.unlink()
                    __rec.sudo().unlink()

            # _rec.sudo().document_ids.unlink()
            # _rec.sudo().unlink()
        
        self.state = "Completed"
        
        return True

            

