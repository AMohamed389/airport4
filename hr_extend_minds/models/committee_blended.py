from odoo import fields, models, api


class BlendedCommittee(models.Model):
    _inherit = 'committee_employee'
    _rec_name = 'committee_name'
    committee_name = fields.Char(related='x_committee_id.committee_name',string='Committee Name', index=True, tracking=True)
    type_of_committee = fields.Selection([('Internal Committee','Internal Committee'),
                                          ('External Committee','External Committee')],
                                         index=True, tracking=True)
    role_member = fields.Selection([('عضو', 'عضو'), ('مدعو', 'مدعو'), ('مستعان', 'مستعان'),
                                    ('مقرر', 'مقرر'), ('امانة', 'امانة'),
                                    ('رئيس', 'رئيس'), ('سكرتير', 'سكرتير'), ('عضو لجنة فرعية', 'عضو لجنة فرعية')])
    member = fields.Char(string="External Committee Member", index=True, tracking=True)
    allowance_percentage = fields.Selection(related='x_committee_id.allowance_percentage',string="Allowance Percentage",tracking=True, index=True)
    repetition_of_attendance = fields.Integer(string="Repetition of Attendance")
    session_ids = fields.Many2many('committee_session', string='Sessions')
    names = fields.Char(compute='calc')

    @api.onchange('type_of_committee')
    @api.depends('type_of_committee')
    def change_member(self):
        if self.type_of_committee == 'Internal Committee':
            self.member = False
        else:
            self.x_employee_id = False

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('x_staff_id', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)



class CommitteeInherit(models.Model):
    _inherit = 'committee'
    _rec_name = 'com'
    committee_name = fields.Char(string='Committee Name', index=True, tracking=True)
    allowance_percentage = fields.Selection([('25','25'),('50','50'),('75','75'),('100','100')],string="Allowance Percentage",tracking=True, index=True)
    session_ids = fields.One2many('committee_session','committee_session_id')
    com = fields.Char(compute='com_name')

    @api.depends('committee_name','name')
    def com_name(self):
        for rec in self:
            rec.com = rec.committee_name + '/' + rec.name

