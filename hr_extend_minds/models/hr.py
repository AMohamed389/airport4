# -*- coding: utf-8 -*-
from re import T
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
import json
import datetime
import string
import requests
from datetime import date
from odoo.osv import expression

import logging

_logger = logging.getLogger(__name__)


class hrextend(models.Model):
    _inherit = 'hr.employee'

    x_graduation_year = fields.Char(string='Year Of Graduation', index=True, tracking=True)

    x_staff_id = fields.Char(string='Staff Id', index=True, tracking=True)

    x_bank_account = fields.Char(string='Bank Account', index=True, tracking=True)

    x_religion = fields.Selection([('Muslim', 'Muslim'), 
                                   ('Christian', 'Christian'),
                                   ('Muslima', 'Muslima'),
                                   ('Christiana', 'Christiana')
                                    ],
                                  string="Religion", store=True, index=True, tracking=True)

    x_social_insurance_number = fields.Char(string='Social Insurance Number', index=True, tracking=True)

    x_social_insurance_status = fields.Selection(
        [('No', 'No'), ('New', 'New'), ('Pending', 'Pending'), ('Done', 'Done')],
        string="Social Insurance Status", store=True,
        index=True, tracking=True)

    # x_job_degree = fields.Selection(
    #     [('Degree 1', 'Degree 1'), ('Degree 2', 'Degree 2'), ('Degree 3', 'Degree 3'),
    #     ('Degree 4', 'Degree 4'), ('Degree 5', 'Degree 5'), ('Degree 6', 'Degree 6')
    #     , ('High Degree', 'High Degree'),('General Manager', 'General Manager')
    #     , ('Excellent Degree', 'Excellent Degree')],
    #     string="Job Degree", store=True,
    #     index=True, tracking=True)

    x_job_degree_id = fields.Many2one('job_degree',string="Degree", index=True, tracking=True)

    x_job_degree_date = fields.Date(string='Degree Date', index=True, tracking=True)

    x_pension_date = fields.Date(string='Pension Date', index=True, tracking=True)

    x_receiving_work_date = fields.Date(string='Receiving Work Date', index=True, tracking=True)

    # x_employee_status = fields.Selection(
    #     [('New', 'New'), ('Hired', 'Hired'), ('Interrupted From Work', 'Interrupted From Work'),
    #      ('Disability', 'Disability'), ('Leave Without Payment', 'Leave Without Payment'),
    #      ('Resigned', 'Resigned'), ('Pension', 'Pension'), ('Terminated', 'Terminated'), ('Death', 'Death')],
    #     string="Employee Status", store=True, index=True, tracking=True, default='New')

    x_hiring_date = fields.Date(string='Hiring Date', index=True, tracking=True)

    x_end_of_service_date = fields.Date(string='End Of Service Date', index=True, tracking=True)

    x_number_of_years = fields.Float(compute="get_number_of_years", string="Number Of Years", store=True)

    x_age = fields.Char(string="Age", compute="get_age_calc", store=True)

    x_employee_training = fields.One2many('employee.training', 'x_employee_id', string="Employee Training", store=True,
                                          index=True)

    x_employee_penalty = fields.One2many('employee.penalty', 'x_employee_id', string="Employee Penalty", store=True,
                                         index=True)

    x_education_certificate_level = fields.Date(string='Education Certificate Date', index=True, tracking=True)

    x_identity_issuer = fields.Char(string='Identity Issuer', index=True, tracking=True)

    x_military_status = fields.Selection([('Postponed','Postponed'),
                                        ('Completed','Completed'),
                                        ('Temporary Exempted','Temporary Exempted'),
                                        ('Final Exempted','Final Exempted'),
                                        ('Not Progressed Yet','Not Progressed Yet')
                                        ], string='Military Status', index=True, tracking=True)

    x_mother_name = fields.Char(string='Mother Name', index=True, tracking=True)

    x_notes = fields.Text(string="Notes", tracking=True, store=True)

    x_military_start_date = fields.Date(string='Military Start Date', index=True, tracking=True)

    x_military_end_date = fields.Date(string='Military End Date', index=True, tracking=True)

    x_has_disability_condition = fields.Boolean(string='Has Disability Condition', index=True, tracking=True)

    x_is_delegated = fields.Boolean(string='Is Delegated', index=True, tracking=True)

    x_delegated_from = fields.Char(string='Delegated From', index=True, tracking=True)

    x_delegated_to = fields.Char(string='Delegated To', index=True, tracking=True)

    x_is_loaned = fields.Boolean(string='Is Loaned', index=True, tracking=True)

    x_loaned_from = fields.Char(string='Loaned From', index=True, tracking=True)

    x_loaned_to = fields.Char(string='Loaned To', index=True, tracking=True)

    x_section_name = fields.Char(index=True, string="Section", compute="_get_section_name", store=True)

    x_administration_name = fields.Char(compute="_get_administration_name", index=True, string="Administration", store=True)

    x_public_administration_name = fields.Char(compute="_get_public_administration_name", index=True, string="Public Administration", store=True)

    x_sector_name = fields.Char(compute="_get_sector_name", index=True, string="Sector", store=True)

    #x_qualitative_group_name = fields.Char(related="job_id.x_qualitative_group_id.name", index=True)

    x_qualitative_group_id = fields.Many2one('qualitative_group',string="Qualitative Group", index=True, tracking=True)

    x_oldest_hiring_date = fields.Date(string='Oldest Hiring Date', index=True, tracking=True)

    x_disability = fields.Char(string="Disability Id Number", index=True, tracking=True)

    x_supervision_job = fields.Many2one('hr.job',string="Supervision Job", domain="[['x_is_supervision_job','=','True']]", index=True, tracking=True)

    x_hr_education_certificate = fields.One2many('hr_education_certificate', 'x_employee_id', string="Education Certificates", store=True,
                                          index=True)
    
    # x_test_image = fields.One2many('test_image', 'employee_id', string="Test Images", store=True,
    #                                       index=True)

    x_job_history = fields.One2many('job_history', 'x_employee_id', string="Job History", store=True,
                                          index=True)
    
    x_seniority_number = fields.Integer(string="Seniority Number", index=True, tracking=True)

    x_committee_employee = fields.One2many('committee_employee', 'x_employee_id', string="Comittees", store=True,
                                          index=True)


    x_document_folder_id = fields.Many2one('documents.folder', string="Document Folder", index=True, tracking=True, ondelete="cascade")

    #x_attachments = fields.One2many('documents.document', 'attachment_id', string="Attachments", compute="_get_attachments", ondelete="cascade")
    x_attachments = fields.One2many('documents.document', string="Attachments", compute="_get_attachments")

    x_current_illegal_earning_date = fields.Char(string="Current Illegal Earning Date", index=True, tracking=True)
    
    x_next_illegal_earning_date = fields.Char(string="Next Illegal Earning Date", index=True, tracking=True)

    job_id = fields.Many2one('hr.job', 'Job Position', domain=lambda self: "[['x_job_degree_id','=', x_job_degree_id],['x_qualitative_group_id','=', x_qualitative_group_id]]", index=True, tracking=True) #TODO vanilla domain removed from job_id ['|', ('company_id', '=', False), ('company_id', '=', company_id)] under hr.employee.base

    x_work_schedule_type = fields.Selection([('Morning','Morning'),
                                        ('Shift','Shift')], string='Work Schedule Type', index=True, required=True, tracking=True)

    resource_calendar_id = fields.Many2one('resource.calendar', domain=lambda self: "['&', ('x_work_schedule_type','=',x_work_schedule_type),'|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True, tracking=True) #TODO vanilla domain removed from resource_calendar_id ['|', ('company_id', '=', False), ('company_id', '=', company_id)],

    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
        ('read and write', 'Read And Write'),
        ('below average qualification', 'Below Average Qualification'),
        ('above average qualification', 'Above Average Qualification'),
        ('postgraduate diploma', 'Postgraduate Diploma'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user", tracking=True, index=True)

    x_company_leaving_reason = fields.Selection([
        ('Reaching The Retirement Age', 'Reaching The Retirement Age'),
        ('Resignation', 'Resignation'),
        ('Death', 'Death'),
        ('Early Pension', 'Early Pension'),
        ('Dismissal Due To A Criminal Sentence', 'Dismissal Due To A Criminal Sentence'),
        ('Dismissal Due To A Court Ruling', 'Dismissal Due To A Court Ruling'),
        ('Transfer', 'Transfer'),
    ], 'Company Leaving Reason', tracking=True, index=True)


    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        # ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced'),
        ('widow and dependent', 'Widow And Dependent'),
        ('married and dependent', 'Married And Dependent'),
        ('divorced and dependent', 'Divorced And Dependent')
    ], string='Marital Status', groups="hr.group_hr_user", tracking=True, index=True)
    employee_training_ids = fields.One2many('employee.training', 'x_employee_id', string='Trainings')
    
    employee_bonus = fields.One2many('employee_bonus', 'employee_id', string='Bonus')
    employee_card = fields.One2many('employee_card', 'employee_id', string='Card')
    

    @api.depends('department_id')
    def _get_section_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Department":
                _rec.x_section_name = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Department":
                _rec.x_section_name = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Department":
                _rec.x_section_name = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Department":
                _rec.x_section_name = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_section_name = None
    
    @api.depends('department_id')
    def _get_administration_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Administration":
                _rec.x_administration_name = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Administration":
                _rec.x_administration_name = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Administration":
                _rec.x_administration_name = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Administration":
                _rec.x_administration_name = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_administration_name = None
    
    @api.depends('department_id')
    def _get_public_administration_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Public Administration":
                _rec.x_public_administration_name = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Public Administration":
                _rec.x_public_administration_name = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_public_administration_name = None

    @api.depends('department_id')
    def _get_sector_name(self):
        for _rec in self:

            if _rec.department_id.x_type == "Sector":
                _rec.x_sector_name = _rec.department_id.name

            elif _rec.department_id.parent_id.x_type == "Sector":
                _rec.x_sector_name = _rec.department_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.x_type == "Sector":
                _rec.x_sector_name = _rec.department_id.parent_id.parent_id.name
            
            elif _rec.department_id.parent_id.parent_id.parent_id.x_type == "Sector":
                _rec.x_sector_name = _rec.department_id.parent_id.parent_id.parent_id.name
            
            else:
                _rec.x_sector_name = None

    def get_number_of_years(self):
        # _logger.info("Maged x_hiring_date !" + str(record.x_hiring_date))
        # _logger.info("Maged x_end_date !" + str(record.x_end_date))
        for record in self:
            if record.x_hiring_date:
                if record.x_end_of_service_date:
                    # _logger.info("Maged delta = record.x_end_date - record.x_hiring_date !")
                    delta = record.x_end_of_service_date - record.x_hiring_date
                    if delta and delta is not None:
                        # _logger.info("Maged delta 1 !" + str(delta))
                        record.x_number_of_years = round((delta.days / 365.25), 2)
                        return record.x_number_of_years
                else:
                    # _logger.info("Maged today = date.today() !")
                    today = date.today()
                    delta = today - record.x_hiring_date
                    if delta and delta is not None:
                        # _logger.info("Maged delta 2 !" + str(delta))
                        record.x_number_of_years = round((delta.days / 365.25), 2)
                        return record.x_number_of_years

        # _logger.info("Maged pass !")
        self.x_number_of_years = 0.0

    @api.depends('birthday')
    def get_age_calc(self):

        for record in self:
            try:
                if record.birthday:
                    #_logger.info("Maged record.birthday ! " + str(record.birthday))
                    today = date.today()
                    offset = int(record.birthday.replace(year=today.year) > today)  # int(True) == 1, int(False) == 0
                    #_logger.info("Maged offset ! " + str(offset))
                    record.x_age = str(date.today().year - record.birthday.year - offset)
                    #_logger.info("Maged record.x_age ! " + str(record.x_age))
                    return record.x_age
                else:
                    record.x_age = '0'
                    return record.x_age
            except Exception as ex:
                #_logger.info("Maged ex ! " + str(ex))
                record.x_age = '0'
                return record.x_age

    @api.constrains('identification_id')
    def _check_id_number_14(self):
        for rec in self:
            if len(str(rec.identification_id)) != 14:
                raise ValidationError("National Id number should be 14 digits !.")

    @api.model   
    def create(self, vals):

    
        #_logger.info(str("hr_employee create vals : ") + str(vals))
        
        # _doc_folder_rec = self.env['documents.folder'].search([('name','=','الموارد البشرية')], limit=1)
        # _logger.info(str("hr_employee create _doc_folder_rec : ") + str(_doc_folder_rec))

        # if not _doc_folder_rec:
        #     _doc_folder_rec = self.env['documents.folder'].search([('name','=','HR')], limit=1)
        #     _logger.info(str("hr_employee create _doc_folder_rec : ") + str(_doc_folder_rec))

        _doc_folder_rec = self.env.ref('documents_hr.documents_hr_folder')

        if _doc_folder_rec:
            
            _folder_name = ""
            if vals.get("name") is not None and vals.get("name"):
                _folder_name = vals.get("name")
                
            if vals['x_staff_id'] is not None and vals['x_staff_id']:
                _folder_name = _folder_name + " " + vals['x_staff_id']

            _doc_folder_parent_create_rec = self.env['documents.folder'].create({
                'name': _folder_name,
                'parent_folder_id': _doc_folder_rec.id,
                # 'parent_folder_id': _doc_folder_rec[0].id
            })

            vals['x_document_folder_id'] = _doc_folder_parent_create_rec.id

            _logger.info(str("hr_employee create _doc_folder_create_rec : ") + str(_doc_folder_parent_create_rec))
            
            _doc_folder_leaves_create_rec = self.env['documents.folder'].create({
                'name': 'أجازات',
                'parent_folder_id': int(_doc_folder_parent_create_rec)
            })

            _doc_folder_general_create_rec = self.env['documents.folder'].create({
                'name': 'مستندات عامة',
                'parent_folder_id': int(_doc_folder_parent_create_rec)
            })

            _doc_folder_penalty_create_rec = self.env['documents.folder'].create({
                'name': 'جزاءات',
                'parent_folder_id': int(_doc_folder_parent_create_rec)
            })

            _doc_folder_grievances_create_rec = self.env['documents.folder'].create({
                'name': 'التظلمات',
                'parent_folder_id': int(_doc_folder_parent_create_rec)
            })

        result = super(hrextend, self).create(vals)
        #_logger.info(str("hr_employee create result : ") + str(result))
        return result

   
    def unlink(self):
        # "your code"

        _doc_folder_rec= None

        for _rec in self:
            if _doc_folder_rec :
                _doc_folder_rec = self.env['documents.folder'].browse(_rec.x_document_folder_id.id)
                _logger.info("hrextend unlink _rec : " + str(_rec))

                _doc_parent_folder_rec = self.env['documents.folder'].search([('parent_folder_id','=',_doc_folder_rec.id)])
                for __rec in _doc_parent_folder_rec:
                    _logger.info("hrextend unlink __rec : " + str(__rec))
                    __rec.document_ids.unlink()
                    __rec.unlink()
                
                _doc_folder_rec.document_ids.unlink()
                _doc_folder_rec.unlink()
        
        
        result = super(hrextend, self).unlink()
        return result


    def _get_attachments(self):
        
        _doc_employee_list = False
        _logger.info("hrextend _get_attachments _doc_employee_list : " + str(_doc_employee_list))

        for _rec in self:
            _logger.info("hrextend _get_attachments _rec : " + str(_rec))
            if _rec.x_document_folder_id:
                _doc_employee_list = self.env['documents.document'].search([('folder_id','=',_rec.x_document_folder_id.id)])
                #_objects = _objects + _doc_employee_list
                _logger.info("hrextend _get_attachments _doc_employee_list : " + str(_doc_employee_list))
               
                _doc_employee_folders_list = self.env['documents.folder'].search([('parent_folder_id','=',_rec.x_document_folder_id.id)])
                _logger.info("hrextend _get_attachments _doc_employee_folders_list : " + str(_doc_employee_folders_list))
                
                for _l in  _doc_employee_folders_list:
                    _doc_parent_list = self.env['documents.document'].search([('folder_id','=',_l.id)])
                    _doc_employee_list = _doc_employee_list + _doc_parent_list

        _logger.info("hrextend _get_attachments _objects : " + str(_doc_employee_list))
            

        _rec.x_attachments = _doc_employee_list


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        _logger.info("hr_employee _name_search name : " + str(name))
        _logger.info("hr_employee _name_search args : " + str(args))
        _logger.info("hr_employee _name_search name_get_uid : " + str(name_get_uid))

        args = args or []
        domain = []
        
        if name:
            domain = ['|','|', ('name', operator, name), ('identification_id', operator, name), ('x_staff_id', operator, name)]
            _logger.info("hr_employee _name_search domain : " + str(domain))

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    _sql_constraints = [('constrain_staff_id', 'UNIQUE (x_staff_id)', 'The staff id is already exists'),
                        ('constrain_identification_id', 'UNIQUE (identification_id)', 'This identification id is already exists')]