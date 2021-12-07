# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class hr_employee_public(models.Model):
    _inherit = 'hr.employee.public'

    x_graduation_year = fields.Char(string='Year Of Graduation', readonly=True)

    x_staff_id = fields.Char(string='Staff Id', readonly=True)

    x_bank_account = fields.Char(string='Bank Account', readonly=True)

    x_religion = fields.Selection([('Muslim', 'Muslim'), 
                                   ('Christian', 'Christian'),
                                   ('Muslima', 'Muslima'),
                                   ('Christiana', 'Christiana')
                                    ],string="Religion", readonly=True)

    x_social_insurance_number = fields.Char(string='Social Insurance Number', readonly=True)

    x_social_insurance_status = fields.Selection([('No', 'No'), ('New', 'New'), ('Pending', 'Pending'), ('Done', 'Done')], string="Social Insurance Status", readonly=True)

    x_job_degree_id = fields.Many2one('job_degree', readonly=True)

    x_job_degree_date = fields.Date(string='Degree Date', readonly=True)

    x_pension_date = fields.Date(string='Pension Date', readonly=True)

    x_receiving_work_date = fields.Date(string='Receiving Work Date', readonly=True)

    x_hiring_date = fields.Date(string='Hiring Date', readonly=True)

    x_end_of_service_date = fields.Date(string='End Of Service Date', readonly=True)

    x_number_of_years = fields.Float(compute="get_number_of_years", readonly=True)

    x_education_certificate_level = fields.Date(string='Education Certificate Date', readonly=True)

    x_identity_issuer = fields.Char(string='Identity Issuer', readonly=True)

    x_military_status = fields.Selection([('Postponed','Postponed'),('Completed','Completed'),('Exempted','Exempted')], readonly=True)

    x_mother_name = fields.Char(string='Mother Name', readonly=True)

    x_notes = fields.Text(string="Notes", readonly=True)

    x_military_start_date = fields.Date(string='Military Start Date', readonly=True)

    x_military_end_date = fields.Date(string='Military End Date', readonly=True)

    x_has_disability_condition = fields.Boolean(string='Has Disability Condition', readonly=True)

    x_is_delegated = fields.Boolean(string='Is Delegated', readonly=True)

    x_delegated_from = fields.Char(string='Delegated From', readonly=True)

    x_delegated_to = fields.Char(string='Delegated To', readonly=True)

    x_is_loaned = fields.Boolean(string='Is Loaned', readonly=True)

    x_loaned_from = fields.Char(string='Loaned From', readonly=True)

    x_loaned_to = fields.Char(string='Loaned To', readonly=True)

    x_qualitative_group_id = fields.Many2one('qualitative_group',string="Qualitative Group", readonly=True)

    x_oldest_hiring_date = fields.Date(string='Oldest Hiring Date', readonly=True)

    x_disability = fields.Char(string="Disability Id Number", readonly=True)

    x_supervision_job = fields.Many2one('hr.job',string="Supervision Job", readonly=True)

    x_seniority_number = fields.Integer(string="Seniority Number", readonly=True)

    x_document_folder_id = fields.Many2one('documents.folder', string="Document Folder", readonly=True)

    x_current_illegal_earning_date = fields.Char(string="Current Illegal Earning Date", readonly=True)
    
    x_next_illegal_earning_date = fields.Char(string="Next Illegal Earning Date", readonly=True)

    job_id = fields.Many2one('hr.job', 'Job Position', readonly=True)


