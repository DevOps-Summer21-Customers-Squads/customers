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
from tests.factory_test import CustomerFactory, AddressFactory
from service.models import Customer, Address, db
from service.routes import app

### -----------------------------------------------------------
### TESTCASE MODULE for Customer and Address
### -----------------------------------------------------------
class TestCustomers(unittest.TestCase):
    """Test Cases for Customer Model"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
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
        """
        Create a Customer only
        """
        cust = Customer(
            first_name="Michael",
            last_name="Jackson",
            user_id="mj",
            password="password",
            active=True,
            address_id="1000",
        )
        self.assertTrue(cust is not None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.first_name, "Michael")
        self.assertEqual(cust.last_name, "Jackson")
        self.assertEqual(cust.user_id, "mj")
        self.assertEqual(cust.password, "password")
        self.assertEqual(cust.active, True)
        self.assertEqual(cust.address_id, "1000")

    def test_create_address(self):
        """
        Create an Address only
        """
        addr = Address(
            street="W 100th St.",
            apartment="OMS",
            city="New York City",
            state="New York",
            zip_code="10030",
            customer_id=1,
        )
        self.assertTrue(addr is not None)
        self.assertEqual(addr.id, None)
        self.assertEqual(addr.street, "W 100th St.")
        self.assertEqual(addr.apartment, "OMS")
        self.assertEqual(addr.city, "New York City")
        self.assertEqual(addr.zip_code, "10030")

    def test_add_customer_and_address(self):
        """
        Create a Customer (and associated Address)
        """
        custs = Customer.all()
        self.assertEqual(custs, [])
        cust = Customer(
            first_name="Joanna",
            last_name="Wang",
            user_id="jwang",
            password="devops",
            active=True
        )
        self.assertTrue(cust is not None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.address_id, None)
        cust.save()
        addr = Address(
            street="100 W 100th St.",
            apartment="Taipei 101",
            city="Taipei",
            state="Taiwan",
            zip_code="10035",
        )
        addr.customer_id = cust.customer_id
        addr.save()
        cust.address_id = addr.id
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(addr.id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)
        self.assertEqual(cust.customer_id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)

    def test_update_customer_password(self):
        """
        Update the Password of a Customer
        """
        customer = Customer(
            first_name="Joanna",
            last_name="Wang",
            user_id="jwang",
            password="devops",
            active=True,
            address_id=0,
        )
        customer.save()
        self.assertEqual(customer.customer_id, 1)
        customer.password = "devops is cool"
        customer.save()
        self.assertEqual(customer.customer_id, 1)
        customer = Customer.all()
        self.assertEqual(len(customer), 1)
        self.assertEqual(customer[0].password, "devops is cool")

    def test_delete_customer(self):
        """
        Delete a Customer (and associated Address)
        """
        customer = Customer(first_name="Joanna",
                            last_name="Wang",
                            user_id="joannawang",
                            password="password",
                            active=True)
        customer.save()
        address = Address(street="50 St. 500 Lane",
                          apartment="234",
                          city="New York",
                          state="New York",
                          zip_code="10110")
        address.customer_id = customer.customer_id
        address.save()
        customer.address_id = address.id
        customer.save()
        self.assertEqual(len(Customer.all()), 1)
        self.assertEqual(len(Address.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
        self.assertEqual(len(Address.all()), 0)


    def test_remove_all_customer(self):
        """
        Delete all Customers
        """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.save()
        _ = Customer.remove_all()
        self.assertEqual(len(Customer.all()), 0)

    def test_activate_customer(self):
        """
        Activate a customer
        """
        customer = Customer(
            first_name="Shuhong",
            last_name="Cai",
            user_id="sc8540@nyu.edu",
            password="password",
            active=False
        )
        customer.save()
        self.assertEqual(customer.active, False)
        customer.active = True
        self.assertEqual(customer.active, True)

    def test_deactivate_customer(self):
        """
        Deactivate a customer
        """
        customer = Customer(
            first_name="Shuhong",
            last_name="Cai",
            user_id="sc8540@nyu.edu",
            password="password",
            active=True
        )
        customer.save()
        self.assertEqual(customer.active, True)
        customer.active = False
        self.assertEqual(customer.active, False)

    def test_list_customers(self):
        """
        List all Customers
        """
        cust1 = Customer(
            first_name="Shuhong",
            last_name="Cai",
            user_id="sc8540@nyu.edu",
            password="gmt+8",
            active=True
        )
        cust1.save()
        cust2 = Customer(
            first_name="Teng",
            last_name="Zhang",
            user_id="tz2179@nyu.edu",
            password="ANingbo",
            active=True,
        )
        cust2.save()
        all_customers = Customer.all()
        self.assertEqual(len(all_customers), 2)

    def test_find_customer_by_id(self):
        """
        Find a Customer by ID
        """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.save()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 3)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].customer_id)
        logging.debug(customer)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.customer_id, customers[1].customer_id)
        self.assertEqual(customer.password, customers[1].password)

    def test_find_by_first_name(self):
        """
        Find a Customer by First Name
        """
        cust1 = Customer(
            first_name="Li",
            last_name="Du",
            user_id="ld2342@nyu.edu",
            password="gmt+8",
            active=True
        )
        cust1.save()
        cust2 = Customer(
            first_name="Teng",
            last_name="Zhang",
            user_id="tz2179@nyu.edu",
            password="ANingbo",
            active=True,
        )
        cust2.save()
        customers = Customer.find_by_first_name("Li")
        self.assertEqual(customers[0].last_name, "Du")
        self.assertEqual(customers[0].user_id, "ld2342@nyu.edu")
        self.assertEqual(customers[0].active, True)

    def test_find_by_last_name(self):
        """
        Find a Customer by Last Name
        """
        cust1 = Customer(
            first_name="Li",
            last_name="Du",
            user_id="ld2342@nyu.edu",
            password="gmt+8",
            active=True
        )
        cust1.save()
        cust2 = Customer(
            first_name="Teng",
            last_name="Zhang",
            user_id="tz2179@nyu.edu",
            password="ANingbo",
            active=True,
        )
        cust2.save()
        customers = Customer.find_by_last_name("Du")
        self.assertEqual(customers[0].first_name, "Li")
        self.assertEqual(customers[0].user_id, "ld2342@nyu.edu")
        self.assertEqual(customers[0].active, True)

    def test_find_by_active(self):
        """
        Find a Customer by Active Status
        """
        cust1 = Customer(
            first_name="Li",
            last_name="Du",
            user_id="ld2342@nyu.edu",
            password="gmt+8",
            active=True
        )
        cust1.save()
        cust2 = Customer(
            first_name="Teng",
            last_name="Zhang",
            user_id="tz2179@nyu.edu",
            password="ANingbo",
            active=False,
        )
        cust2.save()
        customers = Customer.find_by_active(True)
        self.assertEqual(customers[0].last_name, "Du")
        self.assertEqual(customers[0].user_id, "ld2342@nyu.edu")

    def test_find_by_user_id(self):
        """
        Find a Customer by user id
        """
        cust1 = Customer(
            first_name="Li",
            last_name="Du",
            user_id="ld2342@nyu.edu",
            password="gmt+8",
            active=True
        )
        cust1.save()
        cust2 = Customer(
            first_name="Teng",
            last_name="Zhang",
            user_id="tz2179@nyu.edu",
            password="ANingbo",
            active=False,
        )
        cust2.save()
        customers = Customer.find_by_user_id("ld2342@nyu.edu")
        self.assertEqual(customers[0].last_name, "Du")

    def test_delete_address(self):
        """
        Delete an Address
        """
        customer = CustomerFactory()
        customer.save()
        address = AddressFactory()
        address.customer_id = customer.customer_id
        address.save()
        customer.address_id = address.id
        customer.save()
        self.assertEqual(len(Customer.all()), 1)
        self.assertEqual(len(Address.all()), 1)

        # delete one address and make sure it isn't in the database
        address.delete(address.id)
        self.assertEqual(len(Customer.all()), 1)
        self.assertEqual(len(Address.all()), 0)

    def test_remove_all_addresses(self):
        """ Remove all addresses """
        custs = Customer.all()
        self.assertEqual(custs, [])
        cust = Customer(
            first_name="Joanna",
            last_name="Wang",
            user_id="joannawang",
            password="password",
            active=True
        )
        self.assertTrue(cust is not None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.address_id, None)

        cust.save()

        addr = Address(
            street="50 St. 500 Lane",
            apartment="345",
            city="New York",
            state="New York",
            zip_code="10110",
        )
        addr.customer_id = cust.customer_id
        addr.save()
        all_addresses = Address.all()
        self.assertEqual(len(all_addresses), 1)

        addr.remove_all()
        all_addresses = Address.all()
        self.assertEqual(len(all_addresses), 0)
