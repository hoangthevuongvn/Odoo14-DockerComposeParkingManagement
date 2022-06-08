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
    company = fields.Char(string='Company', required = True)
    user_rel = fields.One2many('parking.rfid','rfid_rel', string='RFID', store=True)
    rfid_number = fields.Integer(string = 'RFIDS')
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
        print('XXXXXXX')
        print(rfid_infor.search([]))
        for i in rfid_infor.search([]):
            print(i.id_number)
        # all_rfid_infor = rfid_infor.search([('id', '=', int(self.user_rel))], limit=1)
        # print("All rfid_infor: ", all_rfid_infor.id_number)
    
    @api.onchange("user_rel")
    def compute_rfid_number(self):
            print(self.user_rel.id_number)
            self.rfid_number = self.user_rel.id_number
            
    

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
                                                                    ('daily','Daily'),])
    rf_vehicle_type = fields.Selection(string='Vehicle_type',selection=[('car', 'Car'),
                                                                         ('moto','Moto')]
                                                            ,related='rfid_rel.user_vehicle_type', readonly=False, store=True)
                                                          
    rfid_check_rel = fields.One2many('parking.checktagid','check_tag_rel', String = 'RFID Check Tag Rel')
    rfid_ticket_rel = fields.One2many('parking.ticket_management','ticket_rf_rel', String = 'RFID Ticket Rel')
    status = fields.Boolean('Status', default=False)
    count = fields.Integer()
    price = fields.Float('Price')
    
    _sql_constraints = [('id_number_unique', 'unique(id_number)', "id number be unique!")]
    
    
            
class CheckTagID(models.Model):
    _name = 'parking.checktagid'
    _description = 'Check Tag Id'
    _rec_name = 'check_tag_rel'
    
    check_tag_rel = fields.Many2one('parking.rfid', String='Check TagID Rel')
    # count_status = fields.Integer(related='check_tag_rel.count')
    count_status = fields.Integer()
    time_in = fields.Datetime('Time in')
    time_out = fields.Datetime('Time out')
    total_time = fields.Float('Total time', compute='compute_time', default=0)
    cash = fields.Float('Cash', default = 0, compute='compute_cash', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    _sql_constraints=[('check_time_out', 'CHECK(time_out > time_in)', "The time out must be greater than time in!")]
    #rằng buộc phía database
    
    @api.depends('total_time')
    def compute_cash(self):
        for r in self:
            if r.total_time > 0 and r.check_tag_rel.ticket_type:
                print(r.time_out.day - r.time_in.day)
                if r.check_tag_rel.ticket_type == 'daily':
                    if r.check_tag_rel.rf_vehicle_type == 'moto':
                        r.cash = 5000 
                    if r.check_tag_rel.rf_vehicle_type == 'car':
                        r.cash = 20000*r.total_time
    
                else:
                    r.cash = 0
            else:
                r.cash = 0
    
    @api.depends('time_out')
    def compute_time(self):
        for i in self:
            if i.time_out and i.time_in:
                a = i.time_out - i.time_in
                print(i.time_in)
                print(a.total_seconds())
                i.total_time = a.total_seconds()/3600
            else:
                i.total_time = 0

            
    # @api.constrains('time_out') # rằng buộc phía server
    # def check_time_out(self):
    #     for r in self:
    #         if r.time_in and r.time_out:
    #             if r.time_out < r.time_in:
    #                 raise ValidationError('Time out must be greater than time in!')
            
    
    
            
                
