import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.config.errors import ResourceNotFound
from src.entities.models.order_status_entity import OrderStatus, Status, PaymentStatus
from src.interfaces.gateways.order_status_gateway_interface import IOrderStatusGateway
from src.interfaces.use_cases.order_status_usecase_interface import OrderStatusUseCaseInterface
from src.usecases.order_status_usecase import OrderStatusUseCase
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


class MockUsecase(OrderStatusUseCaseInterface):
    pass


order_status_repo = MockRepository()
order_status_usecase = OrderStatusUseCase(order_status_repo)


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_order_status():
    return OrderStatusHelper.generate_order_status_entity()


@pytest.fixture
def generate_new_order_status_dto():
    return OrderStatusHelper.generate_order_status_request()


@pytest.fixture
def generate_multiple_orders_status():
    return OrderStatusHelper.generate_multiple_order_status_entities()


def test_should_allow_register_order_status(generate_new_order_status_dto, unstub):
    order_status_dto = generate_new_order_status_dto
    order_status_entity = OrderStatus.create_new_order_status(
        order_id=order_status_dto.order_id
    )

    when(order_status_repo).create_order_status(ANY(OrderStatus)).thenReturn(order_status_entity)

    created_order_status = order_status_usecase.create_order_status(order_status_dto)

    assert created_order_status is not None
    assert order_status_dto.order_id == created_order_status.order_id


def test_should_allow_retrieve_order_status_by_id(generate_new_order_status_dto, unstub):
    order_status = generate_new_order_status_dto
    order_status_id = order_status.order_id

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(order_status)

    retrieved_order_status = order_status_usecase.get_by_id(order_status_id)

    verify(order_status_repo, times=1).get_by_id(order_status_id)

    assert order_status.order_id == retrieved_order_status.order_id


def test_should_allow_retrieve_order_status(generate_new_order_status_dto, unstub):
    order_status = generate_new_order_status_dto
    order_status_id = order_status.order_id

    when(order_status_repo).get_order_status(ANY(uuid.UUID)).thenReturn(order_status)

    retrieved_order_status = order_status_usecase.get_order_status(order_status_id)

    verify(order_status_repo, times=1).get_order_status(order_status_id)

    assert order_status.order_id == retrieved_order_status.order_id


def test_should_raise_exception_invalid_id(unstub):
    order_status_id = uuid.uuid4()

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn()

    try:
        order_status_usecase.get_by_id(order_status_id)
        assert False
    except ResourceNotFound:
        assert True

    verify(order_status_repo, times=1).get_by_id(order_status_id)


def test_should_allow_list_ongoing_orders(generate_multiple_orders_status, unstub):
    orders_status_list = generate_multiple_orders_status
    for order in orders_status_list:
        order.order_status = Status.IN_PROGRESS

    when(order_status_repo).list_ongoing_orders().thenReturn(orders_status_list)

    result = order_status_usecase.list_ongoing_orders()

    verify(order_status_repo, times=1).list_ongoing_orders()

    assert type(result) == list
    assert len(result) == len(orders_status_list)
    for order_status in orders_status_list:
        assert order_status in result
        assert order_status.order_status is not Status.PENDING
        assert order_status.order_status is not Status.FINALIZED


def test_should_allow_confirm_order(generate_new_order_status, unstub):
    old_order_status = generate_new_order_status
    old_order_id = old_order_status.order_id

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_order_status)
    when(order_status_repo).update(ANY(uuid.UUID), ANY(OrderStatus)).thenReturn(old_order_status)

    updated_order_status = order_status_usecase.confirm_order(old_order_id)

    assert updated_order_status is not None
    assert updated_order_status.order_id == old_order_status.order_id
    assert updated_order_status.order_status == Status.CONFIRMED


def test_should_allow_update_order_status_in_progress(generate_new_order_status, unstub):
    old_order_status = generate_new_order_status
    old_order_id = old_order_status.order_id

    old_order_status.order_status = Status.CONFIRMED

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_order_status)
    when(order_status_repo).update(ANY(uuid.UUID), ANY(OrderStatus)).thenReturn(old_order_status)

    updated_order_status = order_status_usecase.change_order_status_in_progress(old_order_id, PaymentStatus.CONFIRMED)

    assert updated_order_status is not None
    assert updated_order_status.order_id == old_order_status.order_id
    assert updated_order_status.order_status == Status.IN_PROGRESS


def test_should_allow_update_order_status_ready(generate_new_order_status, unstub):
    old_order_status = generate_new_order_status
    old_order_id = old_order_status.order_id

    old_order_status.order_status = Status.IN_PROGRESS

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_order_status)
    when(order_status_repo).update(ANY(uuid.UUID), ANY(OrderStatus)).thenReturn(old_order_status)

    updated_order_status = order_status_usecase.change_order_status_ready(old_order_id)

    assert updated_order_status is not None
    assert updated_order_status.order_id == old_order_status.order_id
    assert updated_order_status.order_status == Status.READY


def test_should_allow_update_order_status_finalized(generate_new_order_status, unstub):
    old_order_status = generate_new_order_status
    old_order_id = old_order_status.order_id

    old_order_status.order_status = Status.READY

    when(order_status_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_order_status)
    when(order_status_repo).update(ANY(uuid.UUID), ANY(OrderStatus)).thenReturn(old_order_status)

    updated_order_status = order_status_usecase.change_order_status_finalized(old_order_id)

    assert updated_order_status is not None
    assert updated_order_status.order_id == old_order_status.order_id
    assert updated_order_status.order_status == Status.FINALIZED


def test_should_allow_list_orders_status(generate_multiple_orders_status, unstub):
    orders_status_list = generate_multiple_orders_status

    when(order_status_repo).get_all().thenReturn(orders_status_list)

    result = order_status_usecase.get_all()

    verify(order_status_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(orders_status_list)
    for order_status in orders_status_list:
        assert order_status in result


def test_should_allow_list_empty_orders_status(unstub):
    when(order_status_repo).get_all().thenReturn(list())

    result = order_status_usecase.get_all()

    assert result == list()
    verify(order_status_repo, times=1).get_all()


def test_should_allow_remove_order_status(unstub):
    order_id = uuid.uuid4()

    when(order_status_repo).remove_order_status(ANY(uuid.UUID)).thenReturn()

    order_status_usecase.remove_order_status(order_id)

    verify(order_status_repo, times=0).remove_order_status(order_id)
