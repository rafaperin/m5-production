Feature: Order Status Management

  Scenario: Create a new order status
    Given I submit a new order status data
    Then the order status should be created successfully

  Scenario: Get order status by ID
    Given there is a order status with a specific ID
    When I request to get the order status by ID
    Then I should receive the order status details by ID

  Scenario: Get order status
    Given there is an order status
    When I request to get the order status
    Then I should receive the order status details

  Scenario: Get ongoing order status
    Given there is an ongoing order status
    When I request to get the ongoing order status
    Then I should receive the ongoing order status details

  Scenario: Get all orders status
    Given there are existing orders status in the system
    When I request to get all orders status
    Then I should receive a list of orders status

  Scenario: Update order status
    Given there is an order status without status
    When I request to update the order status to in progress
    Then the order status is successfully updated

  Scenario: Remove an order status
    Given there is an order status on database with specific id
    When I request to remove an order
    Then the order data is successfully removed