# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ParkingUser(models.Model):
    _name = 'parking.user'
    _description = 'Parking User'
    # _rec_name = 'rfid_number'
 
    
    name = fields.Char(string='Full name', required=True)
    
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'),
                                                        ('female', 'Female')])
    dob = fields.Date(string='Date of birth', required=True)
    address = fields.Char(string='Address')
    company = fields.Char(string='Company', requied = True)
    user_rel = fields.One2many('parking.rfid','rfid_rel', string='RFID', store=True, readonly=True)
    rfid_number = fields.Integer(string = 'RFIDS', compute='compute_rfid_number')
    #Vehicle
    license_plate = fields.Char(string='License plate', required=True)
    brand = fields.Char(string='Vehicle brand', required=True)
    color = fields.Selection(string='Color', selection=[('red', 'Red'),('black', 'Black'),
                                                        ('white','White'),('yellow', 'Yellow')])
    user_vehicle_type = fields.Selection(string='Vehicle_type', selection=[('car', 'Car'),
                                                                    ('moto','Moto')]) 
    sql_constraints = [('license_plate_unique', 'unique(license_plate)', "Licence be unique!")]
    
    
    
    def get_all_rfid(self):
        # Khởi tạo đối tượng parking.rfid (đây là một recordset rỗng của model parking.rfid)
        rfid_infor = self.env['parking.rfid']
        all_rfid_infor = rfid_infor.search([('id', '=', int(self.user_rel))], limit=1)
        print("All rfid_infor: ", all_rfid_infor.id_number)
    
    @api.depends("user_rel")
    def compute_rfid_number(self):
        for record in self:
            record.rfid_number = record.user_rel.id_number
            
    @api.constrains('dob')
    def _check_dob(self):
        for r in self:
            if r.dob > fields.Date.today():
                raise ValidationError('Date of Birth must be in the past')
                    
    
class ParkingRFID(models.Model):
    _name = 'parking.rfid'
    _description = 'Parking RFID'
    _rec_name = 'id_number' #hien thi ten record la gia tri cua truong id_number 
    
    rfid_rel = fields.Many2one('parking.user', string='RFID user')
    id_number = fields.Integer(string='TAG ID')
    ticket_type = fields.Selection(string='Ticket_type', selection=[('monthly', 'Monthly'),
                                                                    ('day','Day'),])
    rf_vehicle_type = fields.Selection(string='Vehicle_type',selection=[('car', 'Car'),
                                                                         ('moto','Moto')]
                                                            ,compute='compute_vehicle_type', readonly=False, store=True)
                                                          
    rfid_check_rel = fields.One2many('parking.checktagid','check_tag_rel', String = 'RFID Check Tag Rel')
    status = fields.Boolean('Status', default=False)
    count = fields.Integer()
    price = fields.Float('Price')
    _sql_constraints = [('id_number_unique', 'unique(id_number)', "id number be unique!")]

    @api.depends('rfid_rel.user_vehicle_type')
    def compute_vehicle_type(self):
        for r in self:
            print(r.rfid_rel.user_vehicle_type)
            self.rf_vehicle_type = r.rfid_rel.user_vehicle_type
    
            


class CheckTagID(models.Model):
    _name = 'parking.checktagid'
    _description = 'Check Tag Id'
    _rec_name = 'check_tag_rel'
    
    check_tag_rel = fields.Many2one('parking.rfid', String='Check TagID Rel')
    # count_status = fields.Integer(related='check_tag_rel.count')
    count_status = fields.Integer()
    time_in = fields.Datetime('Time in')
    time_out = fields.Datetime('Time out')
    total_time = fields.Float('Total time')
    _sql_constraints=[('check_time_out', 'CHECK(time_out > time_in)', "The time out must be greater than time in!")]
    #rằng buộc phía database
    
    
    @api.onchange('time_in','time_out')
    def compute_time(self):
        if self.time_out:
            a = self.time_out - self.time_in
            print(type(a))
            print(a.total_seconds())
            self.total_time = a.total_seconds()/3600
            
    @api.constrains('time_out') # rằng buộc phía server
    def check_time_out(self):
        for r in self:
            if r.time_out < r.time_in:
                raise ValidationError('Time out must be greater than time in!')
            
                
class UserTest(models.Model):
    
    _name='user.test'


    username = fields.Char(string='user')
    password = fields.Char(string='password')
    
    
    @api.constrains('dob')
    def _check_user(self):
        for r in self:
            if r.user > fields.Date.today():
                raise ValidationError('Date of Birth must be in the past')