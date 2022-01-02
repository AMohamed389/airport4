# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr
import json
import datetime
import string
import requests

import logging
_logger = logging.getLogger(__name__)


class action (models.Model):
    _name = 'action'
    _rec_name ='taskname'
  
    
    
    name = fields.Selection([ ('Excute Python', 'Excute Python') ], string='Action')  
    taskname  = fields.Char(string='Name')
    code = fields.Text(string='Python Code')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    
    

    # @api.constrains('code')
    # def _check_python_code(self):
        
    #     for action in self.sudo().filtered('code'):
    #         msg = test_python_expr(expr=action.code.strip(), mode="exec")
    #         if msg:
    #             raise ValidationError(msg)

    def run_action_code_multi(self, eval_context=None):
        eval_context ={"self":self,"v":ValidationError,"empid":self.employee_id.id }
        safe_eval(self.code.strip(), eval_context, mode="exec", nocopy=True)  # nocopy allows to return 'action'
        #raise ValidationError( eval_context.get('action'))

    
    
    
    
    
  
    





    _sql_constraints = [('constrainname', 'UNIQUE (taskname)', 'This Action already exists')]
    



    
  
  
