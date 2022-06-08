'''
Created on May 23, 2022

@author: thevuonghc
'''
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ParkingUserWizard(models.TransientModel):
    _name = 'parking.user.wizard'
    _inherit='parking.user'
    
class ParkingRfidWizard(models.TransientModel):
    _name = 'parking.rfid.wizard'
    _inherit = 'parking.rfid'

# class ParkingRFWizard(models.TransientModel):
#     _name = ''