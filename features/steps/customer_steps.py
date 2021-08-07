from os import getenv
import logging
import json
import requests
import time
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions


WAIT_SECONDS = int(getenv('WAIT_SECONDS', '20'))


@given('the following customers')
def step_impl(context):
    """ Reset the Database and Add Customers in Batch """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/api/customers', headers=headers)
    expect(context.resp.status_code).to_equal(204)

    create_url = context.base_url + '/api/customers'
    for row in context.table:
        data = {
            "user_id": row['user_id'],
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "password": row['password'],
            "active": row['active'] in ['True', 'true', '1'],
            "address": {
                "street": row['street'],
                "apartment": row['apartment'],
                "city": row['city'],
                "state": row['state'],
                "zip_code": row['zip_code'],
                }
            }

        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when('I visit the Home Page')
def step_impl(context):
    """ Access the base URL """
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)


@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.replace(" ", "_").lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)


@when('I press the "{button}" button')
def step_impl(context, button):
    time.sleep(1)
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search-results')
    not_found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.invisibility_of_element(
            (By.XPATH, "//*[text()='{}']".format(name))
        )
    )
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(not_found, True, error_msg)


@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search-results'),
            name
        )
    )
    expect(found).to_be(True)


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash-message'),
            message
        )
    )
    expect(found).to_be(True)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.replace(" ", "_").lower()
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, element_id),
            ''
        )
    )
    expect(found).to_be(True)
    

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.replace(" ", "_").lower()
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.replace(" ", "_").lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.replace(" ", "_").lower()
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, element_id),
            text
        )
    )
    expect(found).to_be(True)

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.replace(" ", "_").lower()
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.replace(" ", "_").lower()
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)
