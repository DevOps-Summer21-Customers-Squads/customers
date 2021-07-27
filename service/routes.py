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
GET /customers/{id} - Return the Customer with a given ID number
POST /customers - Create a new Customer record in the database
PUT /customers/{id} - Update a Customer record in the database
DELETE /customers/{id} - Deletes a Customer record in the database
"""

from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound, BadRequest
from service.models import Customer, Address
from . import status  # HTTP Status Codes

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
    return app.send_static_file("index.html")

### -----------------------------------------------------------
### ADD A NEW CUSTOMER
### -----------------------------------------------------------
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based on the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.save()
    customer_id = customer.customer_id
    address = Address()
    address.deserialize(request.get_json()['address'])
    address.customer_id = customer_id
    address.save()
    customer.address_id = address.id
    customer.save()
    message = customer.serialize()
    location_url = url_for("create_customers", pet_id=customer.customer_id, _external=True)
    app.logger.info("Customer with ID [%s] created.", customer.customer_id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

### -----------------------------------------------------------
### RETRIEVE A Customer
### -----------------------------------------------------------
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s", customer.customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

### -----------------------------------------------------------
### LIST ALL CUSTOMERS
### -----------------------------------------------------------
@app.route("/customers", methods=["GET"])
def list_customers():
    """
    Returns all of the Customers
    """
    app.logger.info("Request for customer list")
    customers = []
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    active = request.args.get("active", 0)
    if first_name:
        customers = Customer.find_by_first_name(first_name)
    elif last_name:
        customers = Customer.find_by_last_name(last_name)
    elif active != 0:
        active = active in ["True", "true"]
        customers = Customer.find_by_active(active)
    else:
        customers = Customer.all()
    results = [c.serialize() for c in customers]
    app.logger.info("Returning %d customers", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

### -----------------------------------------------------------
### UPDATE AN EXISTING CUSTOMERS
### -----------------------------------------------------------
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer based on customer_id and given customer data
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")
    cust = Customer.find(customer_id, filter_activate=False)

    if not cust:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))

    current_active = cust.active

    cust.deserialize(request.get_json())
    cust.customer_id = customer_id

    if current_active != cust.active:
        raise BadRequest("Not allowed to change active field while updating.")
    cust.active = current_active
    cust.save()

    app.logger.info("Customer with ID [%s] updated.", cust.customer_id)

    return make_response(jsonify(cust.serialize()), status.HTTP_200_OK)

### -----------------------------------------------------------
### DELETE A CUSTOMER
### -----------------------------------------------------------
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete an Account based on specified ID
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

### -----------------------------------------------------------
### ACTIVATE AN EXISTING CUSTOMERS
### -----------------------------------------------------------
@app.route("/customers/<int:customer_id>/activate", methods=["PUT"])
def activate_customers(customer_id):
    """
    Activate a Customer
    """
    app.logger.info("Request to activate customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id, filter_activate=False)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.active = True
    customer.customer_id = customer_id
    customer.save()

    app.logger.info("Customer with ID [%s] activated.", customer.customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

### -----------------------------------------------------------
### DEACTIVATE AN EXISTING CUSTOMERS
### -----------------------------------------------------------
@app.route("/customers/<int:customer_id>/deactivate", methods=["PUT"])
def deactivate_customers(customer_id):
    """
    Deactivate a Customer
    """
    app.logger.info("Request to deactivate customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id, filter_activate=False)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.active = False
    customer.customer_id = customer_id
    customer.save()

    app.logger.info("Customer with ID [%s] deactivated.", customer.customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

### -----------------------------------------------------------
### RETRIEVE AN ADDRESS FROM CUSTOMER
### -----------------------------------------------------------
@app.route('/customers/<int:customer_id>/addresses/<int:address_id>', methods=['GET'])
def get_addresses(customer_id, address_id): # customer_id not used but kept for readbility pylint: disable=unused-argument
    """
    Get an Address
    Just an address get returned
    """
    app.logger.info("Request to get an address with id: %s", address_id)
    address = Address.find(address_id)
    if not address:
        raise NotFound("Address with id '{}' was not found.".format(address_id))
    return make_response(jsonify(address), status.HTTP_200_OK)


### -----------------------------------------------------------
### FlUSH THE WHOLE CUSTOMER DATABASE
### -----------------------------------------------------------
@app.route('/customers/flush', methods=['DELETE'])
def customers_reset():
    """ Removes all customers from the database """
    Address.remove_all()
    Customer.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


### -----------------------------------------------------------
### Auxiliary Utilites
### -----------------------------------------------------------
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
