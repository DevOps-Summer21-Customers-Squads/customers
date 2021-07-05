# API Documentation

## Create

- POST /customers
- Request Body :
  - first_name (String)
  - last_name (String)
  - user_id (String)
  - password (String)
  - active (Boolean)
  - address (Json):
    - street (String)
    - apartment (String)
    - city (String)
    - state (String)
    - zip_code (String)

## Get

- GET /customers/customer_id (int)
- Return Body :
  - customer_id (String)
  - first_name (String)
  - last_name (String)
  - user_id (String)
  - password (String)
  - active (Boolean)
  - address (Json):
    - street (String)
    - apartment (String)
    - city (String)
    - state (String)
    - zip_code (String)

## List

- GET /customers?param = {value}

  parameter examples:

  - first_name (String)
  - last_name (String)
  - active (Boolean)
  
  Note: If no filter condition is specified, all existing customers will be returned. 

## Update

- PUT /customers/customer_id (int)
- Body :
  - first_name (String)
  - last_name (String)
  - user_id (String)
  - password (String)
  - address (Json):
    - street (String)
    - apartment (String)
    - city (String)
    - state (String)
    - zip_code (String)

## Delete

- DELETE /customers/customer_id (int)

## Activate

- PUT /customers/customer_id (int)/activate

## Deactivate

- PUT /customers/customer_id (int)/deactivate

## Get Addresses

- GET /customers/customer_id (int)/addresses/address_id (int)

