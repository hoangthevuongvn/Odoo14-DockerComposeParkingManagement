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
    

    
class LoginAPI(http.Controller):


    @http.route(['/user/login/<user_name>/<pswd>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def login_api(self, user_name, pswd, **kw):
        model_name = "user.test"
        dbname = 'OdooDB19'
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('username', '=', user_name),('password', '=', pswd)])
                if rec:
                    response = {
                        "status": "ok",
                        "content": {
                            "name": rec.username,
                            "pass": rec.password
                        }
                    }
                else:
                    response = {
                        "status": "ok",
                        "content": "Wrong login/password"
                        
                    }
     
            
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)
    
    
    
    @http.route(['/user/register/<user_name>/<pswd>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def register_api(self, user_name, pswd, **kw):
        model_name = "user.test"
        dbname = 'OdooDB19'
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('username', '=', user_name)])
                if rec:
                    response = {
                        "status": "ok",
                        "content": "username already exists"
                        
                    }
                else:
                    env[model_name].create({'username': user_name, 'password': pswd})
                    response = {
                        "status": "ok",
                        "content": "register complete",
                        "user": user_name
                    }
                 
     
            
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)
    
class Infor(http.Controller):
    @http.route(['/user/infor/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def infor_handler(self, id, **kw):
        model_name = "user.test"
        dbname = 'OdooDB19'
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                response = {
                    "status": "ok",
                    "content": {
                        "name": rec.username,
                        "id": rec.id,
                    }
                }
        except Exception:
            response = {
              "status": "error",
              "content": "not found"
            }
        return json.dumps(response)
    
class Update(http.Controller):
    @http.route(['/user/update/<id>/<user_name>/<new_user>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def update_handler(self, id, user_name, new_user, **kw):
        model_name = "user.test"
        dbname = 'OdooDB19'
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('username', '=', user_name), ('id', '=', id)])
                if rec:
                    rec.write({'username':new_user})
                    response = {
                        "status": "ok",
                        "content": "update complete",
                        "username": new_user,
                        
                    }
               
     
            
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)

class ListUser(http.Controller):
    @http.route(['/user/getlist'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def List_handler(self, **kw):
        model_name = "user.test"
        dbname = 'OdooDB19'
        listuser = [] 
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with api.Environment.manage(), registry.cursor() as cr:
                env = api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([])
                for r in rec:
                    listuser.append(r.username) 
                print(listuser)
                response = {
                        "status": "ok",
                        "content": {
                            "name": listuser,
                            
                        }
                    }    
        except Exception:
            response = {
              "status": "error",
              "content": "not found"
            }
        return json.dumps(response)
                