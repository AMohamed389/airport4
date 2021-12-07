# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class hr_employee_report(models.TransientModel):
    _name = 'hr_statement_document'
    
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True, tracking=True, index=True)
    x_hr_report_id = fields.Many2one('hr_report', string="HR Report", store=True, tracking=True, index=True)

    is_full_department_name = fields.Boolean(string="Full Department Name")
    is_sector = fields.Boolean(string="Sector", default=True)
    is_public_administartion = fields.Boolean(string="Public Administration")
    is_administration = fields.Boolean(string="Administration")
    is_section = fields.Boolean(string="Section")
    is_manager = fields.Boolean(string="Manager")
    is_staff_id = fields.Boolean(string="Staff Id", default=True)
    is_insurance_number = fields.Boolean(string="Insurance Number", default=True)
    is_qualitative_group = fields.Boolean(string="Qualitative Group", default=True)
    is_degree = fields.Boolean(string="Degree", default=True)
    is_job_position = fields.Boolean(string="Job Position", default=True)
    is_employee_name = fields.Boolean(string="Employee Name", default=True)
    is_supervision_job = fields.Boolean(string="Supervision job")
    is_hiring_date = fields.Boolean(string="Hiring Date", default=True)
    is_birth_date = fields.Boolean(string="Birth Date", default=True)
    is_gender = fields.Boolean(string="Gender", default=True)
    is_pension_date = fields.Boolean(string="Pension Date", default=True)
    is_marital_status = fields.Boolean(string="Marital Status", default=True)
    is_employee_address = fields.Boolean(string="Employee Address", default=True)
    is_national_id = fields.Boolean(string="National Id", default=True)
    is_id_issuer = fields.Boolean(string="National Id Issuer", default=True)
    is_military_status = fields.Boolean(string="Military Statys", default=True)
    is_place_of_birth = fields.Boolean(string="Place Of Birth", default=True)
    is_mother_name = fields.Boolean(string="Mother Name", default=True)
    is_receiving_Working_date = fields.Boolean(string="Receiving Working Date", default=True)
    is_employee_pic = fields.Boolean(string="Employee Pic")
    is_oldest_hiring_date = fields.Boolean(string="Oldest Hiring Date")
    is_training = fields.Boolean(string="Trainings")
    is_penalties = fields.Boolean(string="Penalties")
    is_job_history = fields.Boolean(string="Job History")
    is_education_certificates = fields.Boolean(string="Education Certificates")
    is_committee = fields.Boolean(string="Committees")
    is_education_certificate_level = fields.Boolean(string="Education Certificate Level")
    is_age = fields.Boolean(string="Age")
    is_email = fields.Boolean(string="Email")
    is_phone = fields.Boolean(string="Phone")
    is_mobile_phone = fields.Boolean(string="Mobile Phone")
    is_work_phone = fields.Boolean(string="Work Phone")
    is_all_selected = fields.Boolean(string="Select All")


    def clean_flags(self):
        for _rec in self:
            _rec.is_full_department_name = False
            _rec.is_sector = False
            _rec.is_public_administartion = False
            _rec.is_administration = False
            _rec.is_section = False
            _rec.is_manager = False
            _rec.is_staff_id = False
            _rec.is_insurance_number = False
            _rec.is_qualitative_group = False
            _rec.is_degree = False
            _rec.is_job_position = False
            _rec.is_employee_name = False
            _rec.is_supervision_job = False
            _rec.is_hiring_date = False
            _rec.is_birth_date = False
            _rec.is_gender = False
            _rec.is_pension_date = False
            _rec.is_marital_status = False
            _rec.is_employee_address = False
            _rec.is_national_id = False
            _rec.is_id_issuer = False
            _rec.is_military_status = False
            _rec.is_place_of_birth = False
            _rec.is_mother_name = False
            _rec.is_receiving_Working_date = False
            _rec.is_employee_pic = False
            _rec.is_oldest_hiring_date = False
            _rec.is_training = False
            _rec.is_penalties = False
            _rec.is_job_history = False
            _rec.is_education_certificates = False
            _rec.is_committee = False
            _rec.is_education_certificate_level = False
            _rec.is_age = False
            _rec.is_email = False
            _rec.is_phone = False
            _rec.is_mobile_phone = False
            _rec.is_work_phone = False

    @api.onchange('is_all_selected')
    def _is_all_selected(self):
        for _rec in self:
            if _rec.is_all_selected:
                _rec.is_full_department_name = True
                _rec.is_sector = True
                _rec.is_public_administartion = True
                _rec.is_administration = True
                _rec.is_section = True
                _rec.is_manager = True
                _rec.is_staff_id = True
                _rec.is_insurance_number = True
                _rec.is_qualitative_group = True
                _rec.is_degree = True
                _rec.is_job_position = True
                _rec.is_employee_name = True
                _rec.is_supervision_job = True
                _rec.is_hiring_date = True
                _rec.is_birth_date = True
                _rec.is_gender = True
                _rec.is_pension_date = True
                _rec.is_marital_status = True
                _rec.is_employee_address = True
                _rec.is_national_id = True
                _rec.is_id_issuer = True
                _rec.is_military_status = True
                _rec.is_place_of_birth = True
                _rec.is_mother_name = True
                _rec.is_receiving_Working_date = True
                _rec.is_employee_pic = True
                _rec.is_oldest_hiring_date = True
                _rec.is_training = True
                _rec.is_penalties = True
                _rec.is_job_history = True
                _rec.is_education_certificates = True
                _rec.is_committee = True
                _rec.is_education_certificate_level = True
                _rec.is_age = True
                _rec.is_email = True
                _rec.is_phone = True
                _rec.is_mobile_phone = True
                _rec.is_work_phone = True
                                

    def print_hr_statement_document(self):
        result = self.env.ref('hr_extend_minds.action_report_hr_statement_document').report_action(self)

        _rec_hr_report = self.env['hr_report'].browse(self.x_hr_report_id.id)
        _logger.info("invoice_print _rec_hr_report : " + str(_rec_hr_report))
        if _rec_hr_report:
            _rec_hr_report.state = 'Completed'
            self.env.cr.commit()

        return result

    # def report_action(self):
    #     res = super(hr_employee_report, self).report_action()
    #     #self.write({'print_button_pressed': True})

    #     _rec_hr_report = self.env['hr_report'].browse(self.x_hr_report_id.id)
    #     _logger.info("invoice_print _rec_hr_report : " + str(_rec_hr_report))
    #     if _rec_hr_report:
    #         _rec_hr_report.state = 'Completed'
    #         self.env.cr.commit()

    #     return res



    
