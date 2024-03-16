import uuid
from abc import ABC, abstractmethod
from typing import List

from src.entities.models.order_status_entity import OrderStatus


class IOrderStatusGateway(ABC):
    @abstractmethod
    def get_by_id(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    @abstractmethod
    def get_order_status(self, order_id: uuid.UUID) -> OrderStatus:
        pass

    @abstractmethod
    def get_all(self) -> List[OrderStatus]:
        pass

    @abstractmethod
    def list_ongoing_orders(self) -> List[OrderStatus]:
        pass

    @abstractmethod
    def create_order_status(self, order_in: OrderStatus) -> OrderStatus:
        pass

    @abstractmethod
    def update(self, order_id: uuid.UUID, order_in: OrderStatus) -> OrderStatus:
        pass

    @abstractmethod
    def remove_order_status(self, order_id: uuid.UUID) -> None:
        pass
