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

import uuid
# import logging
# import atexit
# from functools import wraps
from flask import jsonify, request, make_response, abort
from flask_restx import Api, Resource, fields, reqparse#, inputs
from werkzeug.exceptions import NotFound, BadRequest
from service.models import Customer, Address, DataValidationError#, DatabaseConnectionError
from . import status  # HTTP Status Codes

# Import Flask application
from . import app

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

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
### Configure Swagger
### -----------------------------------------------------------
api = Api(app,
          version='1.0.0',
          title='Customer REST API Service',
          description='This is the Customer server.',
          default='customers',
          default_label='Customer operations',
          doc='/apidocs',

          authorizations=authorizations
         )

# Define the model so that the docs reflect what can be sent
create_address_model = api.model('Address', {
    'street': fields.String(required=True, description='Street'),
    'apartment': fields.String(required=True, description='Apartment'),
    'city': fields.String(required=True, description='City'),
    'state': fields.String(required=True, description='State'),
    'zip_code': fields.String(required=True, description='Zip Code')
})

base_customer_model = api.model('BaseCustomerModel', {
    'user_id': fields.String(required=True, description='The unique User ID given by the Customer'),
    'first_name': fields.String(required=True, description='The first name of the Customer'),
    'last_name': fields.String(required=True, description='The last name of the Customer'),
    'password': fields.String(required=True, description='Password'),
    'active': fields.Boolean(required=True, description='Active status')
})

create_customer_model = api.inherit('Customer', base_customer_model, {
    'address': fields.Nested(create_address_model, description='Address of the Customer')
})

address_model = api.inherit('AddressModel', create_address_model, {
    'id': fields.Integer(required=True, description='The system-generated unique Address ID')
})

customer_model = api.inherit('CustomerModel', base_customer_model, {
    'customer_id': fields.Integer(required=True, description='The system-generated unique Customer ID'),
    'address': fields.Nested(address_model, description='Address of the Customer')
})

# query string
customer_args = reqparse.RequestParser()
customer_args.add_argument('user_id', type=str, required=False, \
    location='args', help='List Customers by their User ID')
customer_args.add_argument('first_name', type=str, required=False, \
    location='args', help='List Customers by their first name')
customer_args.add_argument('last_name', type=str, required=False, \
    location='args', help='List Customers by their last name')
customer_args.add_argument('active', type=str, required=False, \
    location='args', help='List Customers by its active status')
customer_args.add_argument('city', type=str, required=False, \
    location='args', help='List Customers by the city in their addresses')
customer_args.add_argument('state', type=str, required=False, \
    location='args', help='List Customers by the state in their addresses')
customer_args.add_argument('zip_code', type=str, required=False, \
    location='args', help='List Customers by zip code in their addresses')


### -----------------------------------------------------------
### Special Error Handlers
### -----------------------------------------------------------
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.warning(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


### -----------------------------------------------------------
### Generate a random API key
### -----------------------------------------------------------
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex

######################################################################
# PATH /customers
######################################################################
@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """
    Handles all interactions with Resource of Customers
    """
    ### -----------------------------------------------------------
    ### ADD A NEW CUSTOMER
    ### -----------------------------------------------------------
    @api.doc('create_customers', security='apikey')
    @api.expect(create_customer_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Customer created successfully')
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based on the data in the body that is posted
        """
        app.logger.info("Request to create a customer")
        check_content_type("application/json")
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.save()
        customer_id = customer.customer_id
        address = Address()
        address.deserialize(api.payload['address'])
        address.customer_id = customer_id
        address.save()
        customer.address_id = address.id
        customer.save()
        message = customer.serialize()
        location_url = api.url_for(CustomerResource, \
            customer_id=customer.customer_id, _external=True)
        app.logger.info("Customer with ID [%s] created.", customer.customer_id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}

    ### -----------------------------------------------------------
    ### LIST ALL CUSTOMERS
    ### -----------------------------------------------------------
    @api.doc('list_customers', security='apikey')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """
        Return all of the Customers that satisfy query constraints
        """
        app.logger.info("Request for customer list")
        customers = []
        args = customer_args.parse_args()
        if args['first_name']:
            app.logger.info('Filtering by first name: %s', args['first_name'])
            customers = Customer.find_by_first_name(args['first_name'])
        elif args['last_name']:
            app.logger.info('Filtering by last name: %s', args['last_name'])
            customers = Customer.find_by_last_name(args['last_name'])
        elif args['active']:
            app.logger.info('Filtering by active status: %s', args['active'])
            active = args['active'] in ["True", "true"]
            customers = Customer.find_by_active(active)
        elif args['user_id']:
            app.logger.info('Filtering by user id: %s', args['user_id'])
            customers = Customer.find_by_user_id(args['user_id'])
        else:
            app.logger.info('Getting all customers')
            customers = Customer.all()
        results = [c.serialize() for c in customers]
        app.logger.info("Returning %d customers", len(results))
        return results, status.HTTP_200_OK

######################################################################
# PATH /customers/{customer_id}
######################################################################
@api.route('/customers/<int:customer_id>')
@api.param('customer_id', 'The User identifier')
class CustomerResource(Resource):
    """
    Handles CRUD of a single Customer
    """
    ### -----------------------------------------------------------
    ### RETRIEVE A Customer
    ### -----------------------------------------------------------
    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer
        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            raise NotFound("Customer with id '{}' was not found.".format(customer_id))

        app.logger.info("Returning customer: %s", customer.customer_id)
        return customer.serialize(), status.HTTP_200_OK
    
    ## -----------------------------------------------------------
    ### DELETE A CUSTOMER
    ### -----------------------------------------------------------
    @api.doc('delete_customers', security='apikey')
    @api.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """
        Delete an Account based on customer ID
        """
        app.logger.info("Request to delete customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()

        app.logger.info("Customer with ID [%s] delete complete.", customer_id)
        return make_response("", status.HTTP_204_NO_CONTENT)


    ### -----------------------------------------------------------
    ### UPDATE A CUSTOMER
    ### -----------------------------------------------------------
    @api.doc('update_customers', security='apikey')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a customer

        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info("Request to update customer with id: %s", customer_id)

        cust = Customer.find(customer_id)
        if not cust:
            abort(status.HTTP_404_NOT_FOUND,
                  "Customer with id '{}' was not found.".format(customer_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload

        current_active = cust.active

        cust.deserialize(data)
        cust.customer_id = customer_id

        if current_active != cust.active:
            raise BadRequest("Not allowed to change active field while updating, \
                please use Activate/Deactivate button.")
        cust.active = current_active
        cust.save()

        Address.update(cust.address_id, request.get_json()['address'])

        app.logger.info("Customer with ID [%s] updated.", cust.customer_id)
        return cust.serialize(), status.HTTP_200_OK


######################################################################
# PATH /customers/<int:customer_id>/activate
######################################################################
@api.route('/customers/<int:customer_id>/activate')
@api.param('customer_id', 'The User identifier')
class ActivateResource(Resource):
    """
    Handles the operation of activating a Customer
    """
    ### -----------------------------------------------------------
    ### ACTIVATE AN EXISTING CUSTOMERS
    ### -----------------------------------------------------------
    @api.doc('activate_customers', security='apikey')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Activate a single Customer
        This endpoint will return a Customer based on it's id
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
        return customer.serialize(), status.HTTP_200_OK


######################################################################
# PATH /customers/<int:customer_id>/deactivate
######################################################################
@api.route('/customers/<int:customer_id>/deactivate')
@api.param('customer_id', 'The User identifier')
class DeactivateResource(Resource):
    """
    Handles the operation of deactivating a Customer
    """
    ### -----------------------------------------------------------
    ### DEACTIVATE AN EXISTING CUSTOMERS
    ### -----------------------------------------------------------
    @api.doc('deactivate_customers', security='apikey')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Deactivate a single Customer
        This endpoint will return a Customer based on it's id
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
        return customer.serialize(), status.HTTP_200_OK

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
