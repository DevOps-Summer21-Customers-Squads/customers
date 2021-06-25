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

"""
Test cases for Customer Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Customer, Address, DataValidationError, db
from service.routes import app

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')

### -----------------------------------------------------------
### TESTCASE MODULE for Customer and Address
### -----------------------------------------------------------
class TestCustomers(unittest.TestCase):
    """Test Cases for Customer Model"""
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

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ### -----------------------------------------------------------
    ### Testcases:
    ### -----------------------------------------------------------
    def test_create_customer(self):
        """ Create a customer and check that it exists """
        cust = Customer (
            first_name="Michael",
            last_name="Jackson",
            user_id="mj",
            password="password",
            address_id="1000",
        )
        self.assertTrue(cust != None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.first_name, "Michael")
        self.assertEqual(cust.last_name, "Jackson")
        self.assertEqual(cust.user_id, "mj")
        self.assertEqual(cust.password, "password")
        self.assertEqual(cust.address_id, "1000")

    def test_create_address(self):
        """ Create an address and check that it exists """
        addr = Address (
            street="W 100th St.",
            apartment="XXX",
            city="New York City",
            state="New York",
            zip_code="10030",
            customer_id=1
        )
        self.assertTrue(addr != None)
        self.assertEqual(addr.id, None)
        self.assertEqual(addr.street, "W 100th St.")
        self.assertEqual(addr.apartment, "XXX")
        self.assertEqual(addr.city, "New York City")
        self.assertEqual(addr.zip_code, "10030")
