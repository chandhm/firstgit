import pdb
import unittest
import os
import sys
import json
import hashlib
import re
import requests
import time
import datetime
import pprint
import urllib
import filecmp
#from flask_paginate import Pagination
# notes.....
#import pdb; pdb.set_trace()
# once in pdb prompt:
#    - print <something>
#     - c <continue>
#     - s <step into>
#     - n <step out>
#     - up <one frame up>
#     - down <one frame down>

tenants = {}
users = {}
baseUrl = "http://localhost:2773/api/v1/"

def get_delta_date(start, delta):
    d = datetime.date(*(int(s) for s in start.split('-')))
    d += datetime.timedelta(days=delta)
    return str(d)

class TestObject(unittest.TestCase):

    setup_done = False

    def setUp(self):
        if self.setup_done:
            pass
        else:
            otp_code = "ABC"
            self.__class__.setup_done = True

    def test_001_server_test(self):
        # Test the Server is Up/Down
        headers = {'content-type': 'application/json'}
        url = baseUrl + "ping"
        r = requests.get(url, headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_002_add_roles(self):
        # ADD SUPER-ADMIN
        body = {
            "role": "SUPER-ADMIN"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "add-user-type"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)

        # ADD ADMIN
        body = {
            "role": "ADMIN"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "add-user-type"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)

        # ADD TENANT-ADMIN
        body = {
            "role": "TENANT-ADMIN"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "add-user-type"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)

        # ADD USER
        body = {
            "role": "USER"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "add-user-type"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_002a_get_all_roles(self):
        # Get all the roles available
        headers = {'content-type': 'application/json'}
        url = baseUrl + "get-roles"
        r = requests.get(url, headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_003_create_tenant(self):
        # create-tenant
        phone = "+917022110099"
        body = {
            "tenant_phone": phone,
            "tenant_name": "Fork Tech",
            "tenant_address": "admin@gmail.com"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "create-tenant"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        body = json.loads(r.text)
        tenants[phone] = body
        self.assertEqual(r.status_code, 200)

    def test_003a_create_tenant(self):
        # create one more tenant
        phone = "+919999900001"
        body = {
            "tenant_phone": phone,
            "tenant_name": "fork",
            "tenant_address": "admin@gmail.com"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "create-tenant"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        body = json.loads(r.text)
        tenants[phone] = body
        self.assertEqual(r.status_code, 200)


    def test_003b_get_all_tenants(self):
        headers = {'content-type': 'application/json'}
        url = baseUrl + "get-tenants"
        r = requests.get(url, headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_003c_update_tenant(self):
        # update-tenant
        phone = "+919999900001"
        tenantId = tenants[phone]["id"]
        body = {
            "tenant_phone": phone,
            "tenant_name": "fork1",
            "tenant_address": "fork1@gmail.com"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "update-tenant/{}".format(tenantId)
        r = requests.put(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_003d_update_tenant(self):
        # update-tenant with phone
        phone = "+919999900001"
        tenantId = tenants[phone]["id"]
        phone = "+919999900002"
        body = {
            "tenant_phone": phone,
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "update-tenant/{}".format(tenantId)
        r = requests.put(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)


    def test_004_user_register(self):
        # user-register
        phone = "+917022110099"
        tenantId = tenants[phone]["id"]
        body = {
            "phone": phone,
            "name": "Basamma",
            "email": "admin@gmail.com",
	    "password": "fork@123",
            "role": "ADMIN",
            "tenant_id": tenantId
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "user-register"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        body = json.loads(r.text)
        users[phone] = body
        self.assertEqual(r.status_code, 200)

    def test_004a_user_register(self):
        # duplicate user-register
        phone = "+918951447145"
        tenantId = tenants[phone]['id']
        body = {
            "phone": phone,
            "name": "byk",
            "email": "basammayk@gmail.com",
            "password":"fork@123",
            "role":"users",
            "tenant_id":tenantId
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "user-register"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 405)
        
    def test_004b_user_register(self):
        # duplicate entry for user
        phone = "+918296583135"
        tenantId = tenants[phone]['id']
        body = {
            "phone": phone,
            "name": "Sachin",
            "email": "basammayk@gmail.com",
            "password": "fork@123",
            "role": "USERS",
            "tenant_id": tenantId
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "user-register"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)
        
    def test_006_user_login(self):
        # user-login
        phone = "+918296583135"
        body = {
            "phone": phone,
            "emailId": "admin@gmail.com",
            "password": "password"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "login"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)
        
    def test_005_update_tenant(self):
        # update-tenant
        phone = "+919999900001"
        tenantId = tenants[phone]["id"]
        body = {
            "tenant_phone": phone,
            "tenant_name": "Fork Tech",
            "tenant_address": "forktech@gmail.com"
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "update-tenant/{}".format(tenantId)
        r = requests.put(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)

    def test_006_create_assessment(self):
        # user-assessment
        phone = "+917022110099"
        tenantId = tenants[phone]["id"]
        adminId = users[phone]["id"]
        body = {
            "admin_id": adminId,
            "tenant_id": tenantId,
            "assessment_name": "test",
	    "duration": "1 hr 40 min",
            "show_result": False,
            "timed": False,
            "negative_mark" : False
            
        }
        headers = {'content-type': 'application/json'}
        url = baseUrl + "create-assessment"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
