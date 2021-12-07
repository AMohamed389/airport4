# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class hr_employee_report(models.TransientModel):
    _name = 'hr_letter_document'
    
    x_employee_id = fields.Many2one('hr.employee', string="Employee", store=True, tracking=True, index=True)
    x_hr_report_id = fields.Many2one('hr_report', string="HR Report", store=True, tracking=True, index=True)
    
    x_destination = fields.Char(string="Destination")



    def print_hr_letter_document(self):
        result = self.env.ref('hr_extend_minds.action_report_hr_letter_document').report_action(self)

        _rec_hr_report = self.env['hr_report'].browse(self.x_hr_report_id.id)
        _logger.info("hr_employee_report _rec_hr_report : " + str(_rec_hr_report))
        if _rec_hr_report:
            _rec_hr_report.state = 'Completed'
            self.env.cr.commit()

        return result
    