import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.entities.models.order_status_entity import OrderStatus, Status
from src.interfaces.gateways.order_status_gateway_interface import IOrderStatusGateway
from tests.utils.order_status_helper import OrderStatusHelper


class MockRepository(IOrderStatusGateway):

    def get_by_id(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    def get_order_status(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    def get_all(self) -> List[OrderStatus]:
        pass

    def list_ongoing_orders(self) -> List[OrderStatus]:
        pass

    def create_order_status(self, order_in: OrderStatus) -> OrderStatus:
        pass

    def update(self, order_id: uuid.UUID, order_in: OrderStatus) -> OrderStatus:
        pass

    def remove_order_status(self, order_id: uuid.UUID) -> None:
        pass


order_status_repo = MockRepository()


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_order_status():
    return OrderStatusHelper.generate_order_status_entity()


@pytest.fixture
def generate_multiple_orders_status():
    return OrderStatusHelper.generate_multiple_order_status_entities()


def test_should_allow_register_order_status(generate_new_order_status, unstub):
    order_status = generate_new_order_status

    when(order_status_repo).create_order_status(ANY(OrderStatus)).thenReturn(order_status)

    created_order_status = order_status_repo.create_order_status(order_status)

    verify(order_status_repo, times=1).create_order_status(order_status)

    assert type(created_order_status) == OrderStatus
    assert created_order_status is not None
    assert created_order_status == order_status
    assert order_status.order_id == created_order_status.order_id
    assert order_status.creation_date == created_order_status.creation_date
    assert order_status.order_status == created_order_status.order_status


def test_should_allow_retrieve_order_status_by_id(generate_new_order_status, unstub):
    order_status = generate_new_order_status
    order_id = order_status.order_id

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order_status)

    retrieved_order_status = order_status_repo.get_by_id(order_id)

    verify(order_status_repo, times=1).get_by_id(order_id)

    assert order_status.order_id == retrieved_order_status.order_id
    assert order_status.creation_date == retrieved_order_status.creation_date
    assert order_status.order_status == retrieved_order_status.order_status


def test_should_allow_list_orders_status(generate_multiple_orders_status, unstub):
    order_statuss_list = generate_multiple_orders_status

    when(order_status_repo).get_all().thenReturn(order_statuss_list)

    result = order_status_repo.get_all()

    verify(order_status_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(order_statuss_list)
    for order_status in order_statuss_list:
        assert order_status in result


def test_should_allow_list_ongoing_orders(generate_multiple_orders_status, unstub):
    orders_status_list = generate_multiple_orders_status
    for order in orders_status_list:
        order.order_status = Status.IN_PROGRESS

    when(order_status_repo).list_ongoing_orders().thenReturn(orders_status_list)

    result = order_status_repo.list_ongoing_orders()

    verify(order_status_repo, times=1).list_ongoing_orders()

    assert type(result) == list
    assert len(result) == len(orders_status_list)
    for order_status in orders_status_list:
        assert order_status in result
        assert order_status.order_status is not Status.PENDING
        assert order_status.order_status is not Status.FINALIZED


def test_should_allow_update_order_status(generate_new_order_status, unstub):
    order_status = generate_new_order_status
    order_id = order_status.order_id

    order_status.order_status = Status.IN_PROGRESS

    when(order_status_repo).update(ANY(uuid.UUID), ANY(OrderStatus)).thenReturn(order_status)

    created_order_status = order_status_repo.update(order_id, order_status)

    verify(order_status_repo, times=1).update(order_id, order_status)

    assert type(created_order_status) == OrderStatus
    assert created_order_status is not None
    assert created_order_status == order_status
    assert order_status.order_status == created_order_status.order_status


def test_should_allow_retrieve_order_status(generate_new_order_status, unstub):
    order_status = generate_new_order_status
    order_id = order_status.order_id

    when(order_status_repo).get_order_status(ANY(uuid.UUID)).thenReturn(order_status)

    retrieved_order_status = order_status_repo.get_order_status(order_id)

    verify(order_status_repo, times=1).get_order_status(order_id)

    assert order_status.order_id == retrieved_order_status.order_id
    assert order_status.creation_date == retrieved_order_status.creation_date
    assert order_status.order_status == retrieved_order_status.order_status


def test_should_allow_remove_order_status(unstub):
    order_status_id = uuid.uuid4()

    when(order_status_repo).remove_order_status(ANY(uuid.UUID)).thenReturn()

    order_status_repo.remove_order_status(order_status_id)

    verify(order_status_repo, times=1).remove_order_status(order_status_id)
