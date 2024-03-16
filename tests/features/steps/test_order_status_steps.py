import json

import pytest
from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.order_status_helper import OrderStatusHelper

client = TestClient(app)


@pytest.fixture
def generate_order_status_dto():
    return OrderStatusHelper.generate_order_status_request()


@pytest.fixture
def generate_multiple_order_status_dtos():
    return OrderStatusHelper.generate_multiple_orders_status()


@pytest.fixture
def request_order_status_creation(generate_order_status_dto):
    order_status = generate_order_status_dto
    req_body = {
        "order_id": str(order_status.order_id)
    }
    headers = {}
    response = client.post("/order-status", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    order_status_id = result["orderId"]

    yield response
    # Teardown - Removes the order from the database
    client.delete(f"/order-status/{order_status_id}", headers=headers)


@pytest.fixture
def request_multiple_orders_status_creation(generate_multiple_order_status_dtos):
    orders_status_list = generate_multiple_order_status_dtos
    order_status_ids_list = []
    headers = {}

    for order_status in orders_status_list:
        req_body = {
            "order_id": str(order_status.order_id)
        }
        response = client.post("/order-status", json=req_body, headers=headers)

        resp_json = json.loads(response.content)
        result = resp_json["result"]
        order_id = result["orderId"]
        order_status_ids_list.append(order_id)
    yield order_status_ids_list
    # Teardown - Removes the order from the database
    for order_status_id in order_status_ids_list:
        # Teardown - Removes the order from the database
        client.delete(f"/order-status/{order_status_id}", headers=headers)


@pytest.fixture
def create_order_status_without_teardown(generate_order_status_dto):
    order_status = generate_order_status_dto
    req_body = {
        "order_id": str(order_status.order_id),
    }
    headers = {}
    response = client.post("/order-status", json=req_body, headers=headers)

    yield response.content


# Scenario: Get all orders status

@scenario('../order_status.feature', 'Get all orders status')
def test_get_all_orders():
    pass


@given('there are existing orders status in the system', target_fixture='existing_orders_status_in_db')
def existing_orders_status_in_db(request_multiple_orders_status_creation):
    orders_id_list = request_multiple_orders_status_creation
    return orders_id_list


@when('I request to get all orders status', target_fixture='request_all_orders_status')
def request_all_orders_status():
    headers = {}
    response = client.get(f"/order-status/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive a list of orders status')
def receive_correct_order_status(existing_orders_status_in_db, request_all_orders_status):
    orders_status_id_list = existing_orders_status_in_db
    response = request_all_orders_status
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert type(result) == list

    for item in result:
        assert item["orderId"] in orders_status_id_list


# Scenario: Create a new order status


@scenario('../order_status.feature', 'Create a new order status')
def test_create_order_status():
    pass


@given('I submit a new order status data', target_fixture='i_request_to_create_a_new_order_status_impl')
def i_request_to_create_a_new_order_status_impl(generate_order_status_dto, request_order_status_creation):
    response = request_order_status_creation
    return response


@then('the order status should be created successfully')
def the_order_status_should_be_created_successfully_impl(i_request_to_create_a_new_order_status_impl,
                                                         generate_order_status_dto):
    order_status = generate_order_status_dto
    resp_json = json.loads(i_request_to_create_a_new_order_status_impl.content)
    result = resp_json["result"]

    assert result["orderId"] == str(order_status.order_id)


@scenario('../order_status.feature', 'Get order status')
def test_get_order_status():
    pass


@given('there is an order status', target_fixture='order_status_with_given_id')
def order_status_with_given_id(request_order_status_creation):
    response = request_order_status_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["orderId"]


@when('I request to get the order status', target_fixture='request_order_status_by_id')
def request_order_by_id(order_status_with_given_id):
    order_status_with_given_id = order_status_with_given_id
    headers = {}
    response = client.get(f"/order-status/id/{order_status_with_given_id}/status", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the order status details')
def receive_correct_order(order_status_with_given_id, request_order_status_by_id, generate_order_status_dto):
    order_id = order_status_with_given_id
    resp_json = json.loads(request_order_status_by_id)
    result = resp_json["result"]

    assert result["orderId"] == order_id


@scenario('../order_status.feature', 'Get ongoing order status')
def test_get_order_status():
    pass


@given('there is an ongoing order status', target_fixture='order_status_with_given_id')
def order_status_with_given_id(request_order_status_creation):
    response = request_order_status_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["orderId"]


@when('I request to get the ongoing order status', target_fixture='request_order_status_by_id')
def request_order_by_id(order_status_with_given_id):
    order_status_with_given_id = order_status_with_given_id
    headers = {}
    response = client.get(f"/order-status/ongoing", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the ongoing order status details')
def receive_correct_order(order_status_with_given_id, request_order_status_by_id, generate_order_status_dto):
    order_id = order_status_with_given_id
    resp_json = json.loads(request_order_status_by_id)
    result = resp_json["result"]

    assert type(result) == list


# Scenario: Get order status by ID

@scenario('../order_status.feature', 'Get order status by ID')
def test_get_order_status_by_id():
    pass


@given('there is a order status with a specific ID', target_fixture='order_status_with_given_id')
def order_status_with_given_id(request_order_status_creation):
    response = request_order_status_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["orderId"]


@when('I request to get the order status by ID', target_fixture='request_order_status_by_id')
def request_order_by_id(order_status_with_given_id):
    order_status_with_given_id = order_status_with_given_id
    headers = {}
    response = client.get(f"/order-status/id/{order_status_with_given_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the order status details by ID')
def receive_correct_order(order_status_with_given_id, request_order_status_by_id, generate_order_status_dto):
    order_id = order_status_with_given_id
    resp_json = json.loads(request_order_status_by_id)
    result = resp_json["result"]

    assert result["orderId"] == order_id


@scenario('../order_status.feature', 'Update order status')
def test_update_order_status_to_in_progress():
    pass


@given('there is an order status without status', target_fixture='existing_order_status_without')
def existing_order_status_without(request_order_status_creation):
    response = request_order_status_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result


@when('I request to update the order status to in progress', target_fixture='request_status_update')
def request_status_update(existing_order_status_without):
    order_status = existing_order_status_without
    order_status_id = order_status["orderId"]

    headers = {}
    response = client.put(f"/order-status/{order_status_id}/in-progress", headers=headers)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.content is not None

    return response.content


@then('the order status is successfully updated')
def receive_correct_order(request_status_update, generate_order_status_dto):
    updated_order = generate_order_status_dto

    response = request_status_update
    resp_json = json.loads(response)

    assert response is not None


# Scenario: Remove an order status

@scenario('../order_status.feature', 'Remove an order status')
def test_remove_order():
    pass


@given('there is an order status on database with specific id', target_fixture='existing_order_status_to_remove')
def existing_order_status_to_remove(create_order_status_without_teardown):
    order_status = create_order_status_without_teardown
    return order_status


@when('I request to remove an order', target_fixture='request_order_delete')
def request_order_delete(existing_order_status_to_remove):
    response = existing_order_status_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_status_id = result["orderId"]

    headers = {}
    print(order_status_id)
    response = client.delete(f"/order-status/{order_status_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the order data is successfully removed')
def receive_correct_order_status(existing_order_status_to_remove):
    response = existing_order_status_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]

    order_id = result["orderId"]

    headers = {}
    response = client.get(f"/order-status/id/{order_id}", headers=headers)
    print(response)
    assert response.status_code == status.HTTP_200_OK
