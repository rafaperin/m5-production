import uuid
from abc import ABC

from src.entities.models.order_status_entity import OrderStatus
from src.entities.schemas.order_status_dto import CreateOrderStatusDTO
from src.interfaces.gateways.order_status_gateway_interface import IOrderStatusGateway


class OrderStatusUseCaseInterface(ABC):
    def __init__(self, order_status_repo: IOrderStatusGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, order_id: uuid.UUID):
        pass

    def get_order_status(self, order_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def list_ongoing_orders(self):
        pass

    def create_order_status(self, input_dto: CreateOrderStatusDTO) -> OrderStatus:
        pass

    def confirm_order(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    def change_order_status_in_progress(self, order_id: uuid.UUID, payment_status: str) -> OrderStatus:
        pass

    def change_order_status_ready(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    def change_order_status_finalized(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    def remove_order_status(self, order_id: uuid.UUID) -> None:
        pass
