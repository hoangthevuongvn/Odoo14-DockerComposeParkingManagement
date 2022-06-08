'''
Created on May 24, 2022

@author: thevuonghc
'''
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UserTest(models.Model):
    
    _name='user.test'
    _description='username'
    username = fields.Char(string='user')
    password = fields.Char(string='password',  states={'edit': [('invisible', False),('readonly', False)],
                                               'show': [('invisible', False),('readonly', True)],
                                               'hidden': [('invisible', True),('readonly', True)]})
    state = fields.Selection(string='Status', selection=[('edit', 'Edit'),
                                                        ('show', 'Show'),
                                                        ('hidden', 'Hidden')],
                                                    default='new')
    
    
    
    # student_level_id = fields.Many2one('student.test.level', string='Level',
                                      
    
    # @api.constrains('dob')
    # def _check_user(self):
    #     for r in self:
    #         if r.user > fields.Date.today():
    #             raise ValidationError('Date of Birth must be in the past')
    
class StudentTest(models.Model):
    
    _name = 'student.test'
    _description = 'name'
    name = fields.Char(string='char')
    
    student_user_rel = fields.Many2one('user.test')
    
    user_name = fields.Char(related='student_user_rel.username', readonly=False, store=True)
    
 
class TestButton(models.Model):
    _name = 'test.button'
    
    
    test1 = fields.Char()
    test2 = fields.Char() 
    
    
    def func3(self):
        self.create([{'test1':'I', 'test2': 'love'}])
        
    def func1(self):
        self.unlink()