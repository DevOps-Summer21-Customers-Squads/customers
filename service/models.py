# Copyright 2016, 2021 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
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
Models for Customers module

Models
------
Customer - Users of eCommerce Website

Attributes:
-----------
customer_id (string) - ID of the customer, generated by the database, UNIQUE
first_name (string) - The first name of the customer
last_name (string) - The last name of the customer
user_id (string) - User ID of the customer, generated by the user, UNIQUE
password (string) - Password of the customer, generated by the user
address_id(int) - ID of the customer's primary address
"""

import logging
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")
db = SQLAlchemy()


def init_db(app):
    """Initialies the SQLAlchemy app"""
    Customer.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""
    pass


### -----------------------------------------------------------
### CLASS Customer
### -----------------------------------------------------------
class Customer(db.Model):
    """
    Class that represents a Customer
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    app = None

    # Table Schema (Attributes)
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    address_id = db.Column(db.Integer, nullable=True)


    ### -----------------------------------------------------------
    ### INSTANCE METHODS
    ### -----------------------------------------------------------
    def __repr__(self):
        return "<Customer %r %r id=[%s]>" % (self.first_name, self.last_name, self.customer_id)

    def serialize(self):
        """
        Serialize a Customer into a dictionary
        """
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_id": self.user_id,
            "password": self.password,
            "active": self.active,
            "address": Address.find(self.address_id)
            }

    def alternative_serialize(self):
        """
        Serialize a Customer into a dictionary (Internal)
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_id": self.user_id,
            "password": self.password,
            "active": self.active,
            }

    def deserialize(self, data):
        """
        Deserialize a Customer from a dictionary
        """
        try:
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.user_id = data['user_id']
            self.password = data['password']
            self.active = data['active']
        except KeyError as error:
            raise DataValidationError("Invalid Customer: Data Missing\n{}".format(error))
        except TypeError as error:
            raise DataValidationError("Invalid Customer: Type Error\n{}".format(error))
        return self

    def save(self):
        """
        Save a Customer
        """
        logger.info('Saving %s %s', self.first_name, self.last_name)
        db.session.add(self)
        db.session.commit()
        logger.info('Customer saved!')


    def delete(self):
        """
        Remove a Customer (and Addresses as well)
        """
        logger.info('Deleting %s %s', self.first_name, self.last_name)
        Address.delete(self.address_id)
        db.session.delete(self)
        db.session.commit()

    ### -----------------------------------------------------------
    ### CLASS METHODS
    ### -----------------------------------------------------------
    @classmethod
    def init_db(cls, app):
        """
        Initialize the database session
        """
        logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """
        Return all of the Customers in the database
        """
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def remove_all(cls):
        """
        Remove all Customers from the database
        """
        for customer in cls.query.all():
            db.session.delete(customer)
        db.session.commit()

    @staticmethod
    def disconnect():
        """
        Close the database session
        """
        db.session.remove()

    @classmethod
    def find(cls, customer_id, filter_activate=True):
        """
        Find a Customer by customer_id
        """
        logger.info('Processing customer lookup for user id %s ...', customer_id)
        if filter_activate:
            return cls.query.filter(cls.customer_id == customer_id and cls.active).first()
        return cls.query.filter(cls.customer_id == customer_id).first()

    @classmethod
    def find_by_first_name(cls, first_name):
        """Returns all Customers with the given first name

        :param name: the first name of the Customers you want to match
        :type name: str

        :return: a collection of Customers with that first name
        :rtype: list

        """
        logger.info("Processing first name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    def find_by_last_name(cls, last_name):
        """Returns all Customers with the given last name

        :param name: the last name of the Customers you want to match
        :type name: str

        :return: a collection of Customers with that last name
        :rtype: list

        """
        logger.info("Processing last name query for %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_active(cls, active=True):
        """Returns all Customers with the given active status

        :param name: the active status of the Customers you want to match
        :type name: str

        :return: a collection of Customers with that active status
        :rtype: list

        """
        logger.info("Processing active status query for %s ...", active)
        return cls.query.filter(cls.active == active)

### -----------------------------------------------------------
### CLASS Address
### -----------------------------------------------------------
class Address(db.Model):
    """
    Class that represents an Address
    """

    app = None

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    apartment = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)

    ### -----------------------------------------------------------
    ### INSTANCE METHODS
    ### -----------------------------------------------------------
    def serialize(self):
        """
        Serialize an Address into a dictionary
        """
        return {
            "id": self.id,
            "street": self.street,
            "apartment": self.apartment,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code
            }

    def deserialize(self, data):
        """
        Deserialize an Address from a dictionary
        """
        try:
            self.street = data['street']
            self.apartment = data['apartment']
            self.city = data['city']
            self.state = data['state']
            self.zip_code = data['zip_code']
        except KeyError as error:
            raise DataValidationError("Invalid Customer: Data Missing\n{}".format(error))
        except TypeError as error:
            raise DataValidationError("Invalid Customer: Type Error\n{}".format(error))
        return self

    def save(self):
        """
        Save an Address
        """
        logger.info('Saving %s %s', self.street, self.apartment)
        if not self.id:
            db.session.add(self)
        db.session.commit()
        logger.info('Address saved!')


    ### -----------------------------------------------------------
    ### CLASS METHODS
    ### -----------------------------------------------------------
    @classmethod
    def all(cls):
        """
        Return all of the Addresses in the database
        """
        logger.info('Processing all Addresses')
        return cls.query.all()

    @classmethod
    def find(cls, addr_id):
        """
        Find an Address by its ID
        """
        logger.info('Looking up Address for id %s ...', addr_id)
        this_address = cls.query.get(addr_id)
        if this_address:
            print(this_address)
        return this_address.serialize()

    @classmethod
    def delete(cls, addr_id):
        """
        Remove a Address from the database
        """
        logger.info('Deleting %s', addr_id)
        db.session.delete(cls.query.get(addr_id))
        db.session.commit()

    @classmethod
    def remove_all(cls):
        """
        Remove all Addresses from the database
        """
        for address in cls.query.all():
            db.session.delete(address)
        db.session.commit()
