# -*- coding: utf-8 -*-
""" Grants """
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import date, datetime, time
import operator
from functools import reduce


class Grants(models.Model):
    """ Grants """
    _name = 'grants'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'grant_type_id'
    _description = 'Grants'

    hr_employee_id = fields.Many2one('hr.employee', string='Employee Name',
                                     index=True, tracking=True, required=True)
    grant_type_id = fields.Many2one('grant_type', index=True, tracking=True,
                                    required=True)
    grant_check = fields.Boolean()
    s_date = fields.Date()
    e_date = fields.Date()
    diagnosis_id = fields.Many2one('employee_diagnosis_type',
                                   string="Diagnosis Type", index=True,
                                   tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", store=True,
                                  tracking=True, index=True, default=lambda
            self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount', index=True, tracking=True)
    document_date = fields.Date(string='Document Date', index=True,
                                tracking=True, required=True)
    submission_date = fields.Date(string='submission Date', index=True,
                                  tracking=True)
    attachment = fields.Binary()

    @api.constrains('grant_type_id', 'amount', 'document_date')
    def _check_grant_type(self):
        """ Validate grant_type """
        for rec in self:
            total_amount = 0.0
            birth_check = 0
            date = str(fields.Datetime.now())
            datem = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            start_year = '%s-07-1' % datem.year
            extra_year = datem.year + 1
            extra_year03 = datem.year + 3
            end_year = '%s-06-30' % extra_year
            end_year03 = '%s-06-30' % extra_year03
            datem2 = datetime.strptime(start_year, "%Y-%m-%d").date()
            datem3 = datetime.strptime(end_year, "%Y-%m-%d").date()
            datem4 = datetime.strptime(end_year03, "%Y-%m-%d").date()
            hr = self.env['grants'].search(
                [('hr_employee_id', '=', rec.hr_employee_id.id)])
            if rec.hr_employee_id:
                if rec.document_date > datem2 and rec.document_date < datem3:
                    if rec.grant_type_id == self.env.ref(
                            "hr_extend_minds.grant_type_02"):
                        rec.s_date=datem2
                        rec.e_date=datem3
                        hr2 = self.env['grants'].search(
                            [('hr_employee_id', '=', rec.hr_employee_id.id),('grant_type_id', '=', self.env.ref(
                                "hr_extend_minds.grant_type_02").id),('s_date', '=', datem2),('e_date', '=',datem3)])
                        for amount in hr2:
                            total_amount += amount.amount
                        if total_amount > 2500:
                            raise ValidationError(_('علاج احد افراد الاسرة حد أقصى 2500 فى السنة المالية.'))
                        else:
                            rec.s_date=datem2
                            rec.e_date=datem3

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_03"):
                    for birth in hr:
                        if birth.grant_type_id == self.env.ref(
                                "hr_extend_minds.grant_type_03"):
                            birth_check += 1
                            if birth_check > 2:
                                raise ValidationError(
                                    _('منحة الولادة حد أقصى مرتين في العمر'))

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_04"):
                    grant_type = self.env['grants'].search(
                        [('hr_employee_id', '=', rec.hr_employee_id.id), (
                            'grant_type_id', '=',
                            self.env.ref(
                                "hr_extend_minds.grant_type_04").id)])
                    for memo in grant_type:
                        if memo.document_date > datem2 and memo.document_date < datem3:
                            birth_check += 1
                    if birth_check > 1:
                        raise ValidationError(
                            _('منحة الامراض المزمنة مرة واحدة كل سنة'))

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_05"):
                    hr = self.env['grants'].search(
                        [('hr_employee_id', '=', rec.hr_employee_id.id), (
                            'grant_type_id', '=',
                            self.env.ref(
                                "hr_extend_minds.grant_type_05").id)])
                    for con in hr:
                        if not self.grant_check:
                            if con.s_date and con.e_date:
                                if rec.document_date < con.e_date:
                                    raise ValidationError(
                                        _('منحة أجهزة تعويضية (نظارة) حد أقصى 300 جنية كل 3 سنوات '))
                            else:
                                rec.s_date = datem2
                                rec.e_date = datem4
                                rec.grant_check = True

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_06"):
                    hr = self.env['grants'].search(
                        [('hr_employee_id', '=', rec.hr_employee_id.id), (
                            'grant_type_id', '=',
                            self.env.ref(
                                "hr_extend_minds.grant_type_06").id)])
                    for con in hr:
                        if not self.grant_check:
                            if con.s_date and con.e_date:
                                if rec.document_date < con.e_date:
                                    raise ValidationError(
                                        _('منحة أجهزة تعويضية (أسنان) حد أقصى 2000 جنية كل 3 سنوات .'))
                            else:
                                rec.s_date = datem2
                                rec.e_date = datem4
                                rec.grant_check = True

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_07"):
                    hr = self.env['grants'].search(
                        [('hr_employee_id', '=', rec.hr_employee_id.id), (
                            'grant_type_id', '=',
                            self.env.ref(
                                "hr_extend_minds.grant_type_07").id)])
                    for con in hr:
                        if not self.grant_check:
                            if con.s_date and con.e_date:
                                if rec.document_date < con.e_date:
                                    raise ValidationError(
                                        _('منحة أجهزة تعويضية (أ طرف صناعى) حد أقصى 12000 جنية كل 3 سنوات .'))
                            else:
                                rec.s_date = datem2
                                rec.e_date = datem4
                                rec.grant_check = True

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_08"):
                    hr = self.env['grants'].search(
                        [('hr_employee_id', '=', rec.hr_employee_id.id), (
                            'grant_type_id', '=',
                            self.env.ref(
                                "hr_extend_minds.grant_type_08").id)])
                    for con in hr:
                        if not self.grant_check:
                            if con.s_date and con.e_date:
                                if rec.document_date < con.e_date:
                                    raise ValidationError(
                                        _('منحة أجهزة تعويضية (سماعة ضعف سمع) حد أقصى 4000 جنية كل 3 سنوات .'))
                            else:
                                rec.s_date = datem2
                                rec.e_date = datem4
                                rec.grant_check = True

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_10"):
                    for birth in hr:
                        if birth.grant_type_id == self.env.ref(
                                "hr_extend_minds.grant_type_10"):
                            birth_check += 1
                            if birth_check > 2:
                                raise ValidationError(
                                    _('منحة الانجاب مرتين في العمر .'))

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_12"):
                    for birth in hr:
                        if birth.grant_type_id == self.env.ref(
                                "hr_extend_minds.grant_type_12"):
                            birth_check += 1
                            if birth_check > 1:
                                raise ValidationError(
                                    _('منحة الزواج مرة واحدة في العمر .'))

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_14"):
                    for birth in hr:
                        if birth.grant_type_id == self.env.ref(
                                "hr_extend_minds.grant_type_14"):
                            birth_check += 1
                            if birth_check > 1:
                                raise ValidationError(
                                    _('منحة وفاة عضو الشركة مرة واحدة في العمر .'))

                if rec.grant_type_id == self.env.ref(
                        "hr_extend_minds.grant_type_11"):
                    na=hr.hr_employee_id.name
                    if hr.hr_employee_id.children:
                        print(hr.hr_employee_id.children)
                        for birth in hr:
                            if birth.grant_type_id == self.env.ref(
                                    "hr_extend_minds.grant_type_11"):

                                birth_check += 1
                                if birth_check > hr.hr_employee_id.children:
                                    raise ValidationError(
                                        _('منحة زواج احد ابناء عضو الشركة مرة واحدة للإبن .'))
                    else:
                        raise ValidationError(
                            _('عضو الشركة %s ليس لديه أبناء.')%na)
