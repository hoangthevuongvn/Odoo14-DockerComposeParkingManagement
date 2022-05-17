# -*- coding: utf-8 -*-
import odoo
from odoo import http,api
from odoo.http import request
import json

class ParkingAPI(http.Controller):
    @http.route('/parking/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })
        
    # @http.route('/user', type='http', auth="user", website=True)
    # def library_books(self):
    #     return request.render('parking_users', {'': request.env['parking.user'].search([]),
    # })
    #



    @http.route(['/parking/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def pet_handler(self, dbname, id, **kw):
        model_name = "parking.user"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                response = {
                    "status": "ok",
                    "content": {
                        "name": rec.name,
                        "gender": rec.gender,
                        "dob": str(rec.dob)
                    }
                }
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)