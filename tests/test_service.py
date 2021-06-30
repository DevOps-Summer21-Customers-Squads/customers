# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### -----------------------------------------------------------
###  Modified by DevOps Course Summer 2021 Customer Team 
###  Members:
###     Du, Li | ld2342@nyu.edu | Nanjing | GMT+8
###     Cai, Shuhong | sc8540@nyu.edu | Shanghai | GMT+8
###     Zhang, Teng | tz2179@nyu.edu | Ningbo | GMT+8
###     Zhang, Ken | sz1851@nyu.edu | Shanghai | GMT+8
###     Wang,Yu-Hsing | yw5629@nyu.edu | Taiwan | GMT+8
### -----------------------------------------------------------


import logging
import unittest
import os
from flask_api import status    # HTTP Status Codes
import uuid
from urllib.parse import quote_plus
from unittest.mock import MagicMock, patch
from tests.factory_test import CustomerFactory, AddressFactory
from service.models import Customer, Address, DataValidationError, db
from service.routes import app
from service.error_handlers import internal_server_error

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')
BASE_URL = "/customers"
CONTENT_TYPE_JSON = "application/json"


### -----------------------------------------------------------
### TESTCASE MODULE for Customer System Server
### -----------------------------------------------------------
class TestCustomerServer(unittest.TestCase):
    """Test Cases for Customer Server"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables
        self.app = app.test_client()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    def _fake_customers(self, num):
        """Factory method to fake customers in batch"""
        customers = []
        for _ in range(num):
            test_customer = CustomerFactory()
            test_address = AddressFactory()
            addr_json = test_address.serialize()
            cust_json = test_customer.alternative_serialize()
            cust_json["address"] = addr_json
            resp = self.app.post(BASE_URL,
                                 json=cust_json,
                                 content_type=CONTENT_TYPE_JSON)
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create Customer')
            new_cust = resp.get_json()
            test_customer.customer_id = new_cust["customer_id"]
            addr = new_cust["address"]
            test_customer.address_id = addr["id"]
            customers.append(test_customer)
        return customers
    
    ### -----------------------------------------------------------
    ### Testcases:
    ### -----------------------------------------------------------
    def test_create_customer(self):
        """
        Create new Customer on Server
        """
        body = {
            "first_name": "Young",
            "last_name": "Nick",
            "user_id": "confused",
            "password": "lakers",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "LA",
                "state": "Cali",
                "zip_code": "100"
            },
            "active": True
        }
        resp = self.app.post(BASE_URL,
                             json=body,
                             content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer['first_name'], "Young", "first_name do not match")
        self.assertEqual(new_customer['last_name'], "Nick", "last_name do not match")
        self.assertEqual(new_customer['user_id'], "confused", "user_id do not match")
        self.assertEqual(new_customer['active'], True, "active status not match")
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()[0]
        self.assertEqual(new_customer['first_name'], "Young", "first_name do not match")
        self.assertEqual(new_customer['last_name'], "Nick", "last_name do not match")
        self.assertEqual(new_customer['user_id'], "confused", "user_id do not match")
        self.assertEqual(new_customer['active'], True, "active status not match")

    def test_index(self):
        """
        Customer Server index call
        """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer_missing_last_name(self):
        """ 
        <Anomaly> Create Customer with Last Name missing
        """
        body = {
            "first_name": "Young",
            "user_id": "confused",
            "password": "lakers",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "LA",
                "state": "Cali",
                "zip_code": "100"
            }
        }
        resp = self.app.post(BASE_URL, 
                             json=body, 
                            content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_missing_street(self):
        """ 
        <Anomaly> Create Customer with Street missing
        """
        body = {
            "last_name": "ken",
            "first_name": "Young",
            "user_id": "confused",
            "password": "lakers",
            "address": {
                "apartment": "100",
                "city": "LA",
                "state": "Cali",
                "zip_code": "100"
            }
        }
        resp = self.app.post(BASE_URL, 
                             json=body, 
                            content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_not_found(self):
        """ 
        <Anomaly> Query non-existent Customer
        """
        self._fake_customers(1)
        resp = self.app.get('/customers/{}'.format("monkey"),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        resp = self.app.get("/customers/100")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer_by_id(self):
        """
        Get a single Customer by ID
        """
        # get the id of a customer
        test_customer = self._fake_customers(1)[0]
        resp = self.app.get("/customers/{}".format(test_customer.customer_id), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["first_name"], test_customer.first_name)

    def test_list_all_customers(self):
        """
        List all Customers
        """
        self._fake_customers(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
    
    def test_query_customer_list_by_first_name(self):
        """
        Query Customers by First Name
        """
        customers = self._fake_customers(10)
        test_first_name = customers[0].first_name
        first_name_customers = [customer for customer in customers if customer.first_name == test_first_name]
        resp = self.app.get(
            BASE_URL, query_string="first_name={}".format(quote_plus(test_first_name))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(first_name_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer["first_name"], test_first_name)

    def test_query_customer_list_by_last_name(self):
        """
        Query Customers by Last Name
        """
        customers = self._fake_customers(10)
        test_last_name = customers[0].last_name
        last_name_customers = [customer for customer in customers if customer.last_name == test_last_name]
        resp = self.app.get(
            BASE_URL, query_string="last_name={}".format(quote_plus(test_last_name))
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(last_name_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer["last_name"], test_last_name)
    
    def test_query_customer_list_by_active(self):
        """
        Query Customers by Active Status
        """
        customers = self._fake_customers(3)
        test_active = customers[0].active
        active_customers = [customer for customer in customers if customer.active == test_active]
        resp = self.app.get(
            BASE_URL, query_string="active={}".format(test_active)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(active_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer["active"], test_active)

    def test_invalid_content_type(self):
        """
        <Anomaly> Create Customer with invalid content type
        """
        body = {
            "first_name": "Young",
            "last_name": "Nick",
            "user_id": "confused",
            "password": "lakers",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "LA",
                "state": "Cali",
                "zip_code": "100"
            },
            "active": True
        }
        resp = self.app.post(BASE_URL,
                             json=body,
                             content_type='text/plain')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_internal_server_error_500(self):
        """
        <Anomaly> Delete non-existent Customer
        """
        resp = self.app.delete('/customers/100', content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_method_request_405(self):
        """
        <Anomaly> Try bad request (method not allowed)
        """
        resp = self.app.delete('/customers', content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_delete_customer(self):
        # create a customer to delete
        test_customer = self._fake_customers(1)[0]

        """ Delete a Customer """
        resp = self.app.delete('/customers/{}'.format(test_customer.customer_id), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        # make sure they are deleted
        resp = self.app.get('/customers/{}'.format(test_customer.customer_id), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_customer(self):
        """
        Deactivate a customer by ID
        """
        # create a Customer to deactivate
        test_customer = self._fake_customers(1)[0]
        # make sure the original customer is active
        self.assertEqual(test_customer.active, True)

        # deactivate the customer
        resp = self.app.put(
            "/customers/{}/deactivate".format(test_customer.customer_id),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        deactivated_customer = resp.get_json()
        self.assertEqual(deactivated_customer["active"], False)