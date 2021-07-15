# DevOps-Summer21-Customers-Squads/customers
[![Build Status](https://travis-ci.com/DevOps-Summer21-Customers-Squads/customers.svg?branch=main)](https://travis-ci.com/DevOps-Summer21-Customers-Squads/customers)

## Introduction
This repository is a project of NYU course **CSCI-GA.2820: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, in **Summer 2021** semester. 

This project is the back-end for an eCommerce website as a RESTful microservice for the registered customers. This microservice supports the complete Create, Read, Update, & Delete (CRUD) lifecycle calls plus List, Query, Activate, and Deactivate. 

## Members

Du, Li | ld2342@nyu.edu | Nanjing | GMT+8 

Cai, Shuhong | sc8540@nyu.edu | Shanghai | GMT+8

Zhang, Teng |  tz2179@nyu.edu | Ningbo | GMT+8 

Zhang, Ken | sz1851@nyu.edu | Shanghai | GMT+8 

Wang,Yu-Hsing | yw5629@nyu.edu | Taiwan | GMT+8 

## Repository Structure
```
├── service
│   ├── __init__.py        - package initializer
│   ├── error_handlers.py  - http error codes
│   ├── models.py          - module with main database models
│   ├── routes.py          - module with service routes
│   └── status.py          - http status codes 
├── tests
│   ├── __init__.py        - package initializer
│   ├── factory_test.py    - factory to fake customer data
│   ├── test_models.py     - test suite for models.py
│   └── test_service.py    - test suite for routes.py
```
### Database Attributes

| Field | Type | Description | Primary Key
| :--- | :--- | :--- | :--- |
| customer_id | Integer | ID (auto-incremented by database) | Yes
| first_name | String | Customer's First Name | No
| last_name | String | Customer's Last Name | No
| user_id | String | Customer's Self-Defined Login ID | No
| password | String | Customer's Self-Defined Login Credential | No
| address_id | Integer | Address ID | No


## Run the Service on Your Local PC

### Prerequisite Installations
Download [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).

### Run the Service in Terminal
Type below commands in your terminal:

```
$ git clone https://github.com/DevOps-Summer21-Customers-Squads/customers.git
$ cd customers
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ honcho start or FLASK_APP=service:app flask run -h 0.0.0.0
```

Now open your browser, you are expected to see the following json response when browsing http://0.0.0.0:5000

```
{"name":"Customer Service API","paths":"http://0.0.0.0:5000/","version":"1.0"}
```
### Run TDD Unit Tests
```
$ nosetests
```
If you want to see the lines of codes not tested, run:
```
$ coverage report -m
```

### Terminate the Service
Before you leave, be reminded to terminate the service by running
```
$ exit
$ vagrant halt
```
If the virtual machine is no longer needed, you can: 
```
$ vagrant destroy
```

## API Documentation
### Create

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

### Get

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

### List

- GET /customers?param = {value}

  parameter examples:

  - first_name (String)
  - last_name (String)
  - active (Boolean)

  Note: If no filter condition is specified, all existing customers will be returned. 

### Update

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

### Delete

- DELETE /customers/customer_id (int)

### Activate

- PUT /customers/customer_id (int)/activate

### Deactivate

- PUT /customers/customer_id (int)/deactivate

### Get Addresses

- GET /customers/customer_id (int)/addresses/address_id (int)
