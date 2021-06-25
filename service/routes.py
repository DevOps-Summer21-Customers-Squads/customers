
# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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
Customer Service

Paths:
------
GET /customers - Return a list of all Customers
GET /pets/{id} - Return the Customer with a given ID number
POST /customers - Create a new Customer record in the database
PUT /pets/{id} - Update a Customer record in the database
DELETE /pets/{id} - Deletes a Pet record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app


### -----------------------------------------------------------
### GET INDEX
### -----------------------------------------------------------
@app.route("/")
def index():
    """
    Root URL response
    """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Customer Service API",
            version="1.0",
            paths=url_for("index", _external=True),
        ),
        status.HTTP_200_OK,
    )


### -----------------------------------------------------------
### ADD A NEW CUSTOMER
### -----------------------------------------------------------
@app.route("/customers", methods=["POST"])
def create_customers():
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", pet_id=customer.customer_id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.customer_id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )