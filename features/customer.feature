
Feature: The customer service back-end
    As a customer service provider
    I need a RESTful catalog service
    So that I can keep track of all my customers



Background: Init Customer Database
    Given the following customers
        | user_id | first_name | last_name | password | street | apartment | city | state | zip_code | active |
        |     1   |      fn1   |     ln1   |   1234   |  s1    |    a1     | c1   |  se1  |  zip1    | True   |
        |     2   |      fn2   |     ln2   |   4321   |  s2    |    a2     | c2   |  se2  |  zip2    | True   |
        |     3   |      fn3   |     ln3   |   6789   |  s3    |    a3     | c3   |  se3  |  zip3    | False  |
        |     4   |      fn4   |     ln4   |   9876   |  s4    |    a4     | c4   |  se4  |  zip4    | False  |



Scenario: The server is running
    When I visit the Home Page
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"



Scenario: List all Customers
    When I visit the Home Page
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "1" in the results
    And I should see "2" in the results
    And I should see "3" in the results
    And I should see "4" in the results
    Then I should see "fn1" in the results
    And I should see "fn2" in the results
    And I should see "fn3" in the results
    And I should see "fn4" in the results
    Then I should see "ln1" in the results
    And I should see "ln2" in the results
    And I should see "ln3" in the results
    And I should see "ln4" in the results
    And I should see "s1, a1, c1, se1 - zip1" in the results
    And I should see "s2, a2, c2, se2 - zip2" in the results
    And I should see "s3, a3, c3, se3 - zip3" in the results
    And I should see "s4, a4, c4, se4 - zip4" in the results
    Then I should see "true" in the results
    And I should see "false" in the results   



Scenario: Create a Customer
    When I visit the Home Page
    And I set the "User ID" to "zsy"
    And I set the "First Name" to "Ken"
    And I set the "Last Name" to "Zhang"
    And I set the "password" to "zsy"
    And I set the "apartment" to "apartment"
    And I set the "street" to "street"
    And I set the "city" to "city"
    And I set the "state" to "state"
    And I set the "ZIP code" to "zip_code"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    Then the "User ID" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "password" field should be empty
    And the "apartment" field should be empty
    And the "street" field should be empty
    And the "city" field should be empty
    And the "state" field should be empty
    And the "ZIP code" field should be empty
    And the "active" field should be empty
    When I press the "Search" button
    Then I should see "zsy" in the results
    And I should see "Ken" in the results
    And I should see "Zhang" in the results
    And I should see "street, apartment, city, state - zip_code" in the results
    And I should see "true" in the results
    

Scenario: Activate and Deactivate a Customer
    When I visit the Home Page
    And I set the "First Name" to "fn1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Customer ID" field
    And I press the "Clear" button
    And I paste the "Customer ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "fn1" in the "First Name" field
    And I should see "True" in the "active" dropdown
    When I press the "Deactivate" button
    Then I should see the message "Customer deactivated."
    And I should see "fn1" in the "First Name" field
    And I should see "False" in the "active" dropdown
    When I press the "Activate" button
    Then I should see the message "Customer activated."
    And I should see "fn1" in the "First Name" field
    And I should see "True" in the "active" dropdown
    
    

Scenario: Delete a Customer
    When I visit the Home Page
    And I set the "First Name" to "fn1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fn1" in the results
    When I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should not see "fn1" in the results

Scenario: Update a Customer
    When I visit the Home Page
    And I set the "First Name" to "fn2"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fn2" in the results
    When I set the "User ID" to "222"
    And I set the "First Name" to "fn2_updated"
    And I set the "Last Name" to "ln2_updated"
    And I set the "password" to "123456"
    And I set the "apartment" to "a2_updated"
    And I set the "street" to "s2_updated"
    And I set the "city" to "c2_updated"
    And I set the "state" to "se2_updated"
    And I set the "ZIP code" to "zip2_updated"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "User ID" to "222"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "fn2_updated" in the results
    And I should see "ln2_updated" in the results
    And I should see "s2_updated, a2_updated, c2_updated, se2_updated - zip2_updated" in the results


