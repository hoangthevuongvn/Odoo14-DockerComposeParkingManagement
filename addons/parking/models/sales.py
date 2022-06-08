'''
Created on May 27, 2022

@author: thevuonghc
'''
import datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class TicketManagement(models.TransientModel):
    
    _name = 'parking.ticket_management'
    _rec_name = 'user'
    
    ticket_rf_rel = fields.Many2one('parking.rfid', string = 'RFID TAG')
    user = fields.Char(store='True')
    activated = fields.Boolean()
    from_date = fields.Date('From Date')
    due_date = fields.Date('Due Date', compute='tinhtoan')
    month_number = fields.Integer('Period')
    payment = fields.Integer('Payment')
    
    
    # @api.depends()
    # def compute_time(self):
        
    # @api.autovacuum
    # def _ondel(self):
    #     # timeout_ago =self.due_date - fields.Date.today
    #     if self.due_date > fields.Date.today:
    #         return self.unlink()
        
    
    
    @api.onchange('month_number')
    def payments(self):
                if self.ticket_rf_rel.rf_vehicle_type == 'car':
                    self.payment = self.month_number*1000000
                if self.ticket_rf_rel.rf_vehicle_type == 'moto':
                    self.payment = self.month_number*100000
        
    
    
    @api.onchange('ticket_rf_rel')
    def getuser(self):
            print("SSSSSSSSSSSSSSS")
            print(self.ticket_rf_rel.rfid_rel.name)
            self.user = self.ticket_rf_rel.rfid_rel.name
            print(self)
            print(type(self))
            # s = i.ticket_rf_rel.rfid_rel.id
            # print(self.env['parking.user'].search([('id', '=', s)]).name)
            #

    @api.depends('from_date','month_number')
    def tinhtoan(self):
        print('XXXXXX')
        for r in self:
            if r.from_date and r.month_number != 0:
                print(r.from_date)
                print(type(r.from_date))
                self.due_date = fields.Date.add(r.from_date,months=r.month_number)
                print(type(r.due_date))
            else:
                r.due_date = fields.Datetime.now()
            
                
                            
    
    