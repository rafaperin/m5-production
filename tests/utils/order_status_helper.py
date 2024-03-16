import uuid
from typing import List

from src.entities.models.order_status_entity import OrderStatus
from src.entities.schemas.order_status_dto import CreateOrderStatusDTO


class OrderStatusHelper:

    @staticmethod
    def generate_order_status_request() -> CreateOrderStatusDTO:
        return CreateOrderStatusDTO(
            order_id=uuid.uuid4()
        )

    @staticmethod
    def generate_multiple_orders_status() -> List[CreateOrderStatusDTO]:
        order_statuss_list = []
        order_status1 = CreateOrderStatusDTO(
            order_id=uuid.uuid4()
        )

        order_status2 = CreateOrderStatusDTO(
            order_id=uuid.uuid4()
        )
        order_statuss_list.append(order_status1)
        order_statuss_list.append(order_status2)
        return order_statuss_list

    @staticmethod
    def generate_order_status_entity() -> OrderStatus:
        return OrderStatus.create_new_order_status(
            order_id=uuid.uuid4()
        )

    @staticmethod
    def generate_multiple_order_status_entities() -> List[OrderStatus]:
        order_statuss_list = []
        order_status1 = OrderStatus.create_new_order_status(
            order_id=uuid.uuid4()
        )

        order_status2 = OrderStatus.create_new_order_status(
            order_id=uuid.uuid4()
        )
        order_statuss_list.append(order_status1)
        order_statuss_list.append(order_status2)
        return order_statuss_list
