import uuid

from src.config.errors import ResourceNotFound

from src.entities.schemas.order_status_dto import CreateOrderStatusDTO
from src.entities.models.order_status_entity import OrderStatus
from src.interfaces.gateways.order_status_gateway_interface import IOrderStatusGateway
from src.interfaces.use_cases.order_status_usecase_interface import OrderStatusUseCaseInterface


class OrderStatusUseCase(OrderStatusUseCaseInterface):
    def __init__(self, order_status_repo: IOrderStatusGateway) -> None:
        self._order_status_repo = order_status_repo

    def get_by_id(self, order_id: uuid.UUID):
        result = self._order_status_repo.get_by_id(order_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_order_status(self, order_id: uuid.UUID):
        result = self._order_status_repo.get_order_status(order_id)

        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._order_status_repo.get_all()

    def list_ongoing_orders(self):
        return self._order_status_repo.list_ongoing_orders()

    def create_order_status(self, input_dto: CreateOrderStatusDTO) -> OrderStatus:
        order_status = OrderStatus.create_new_order_status(input_dto.order_id)
        self._order_status_repo.create_order_status(order_status)
        return order_status

    def confirm_order(self, order_id: uuid.UUID) -> OrderStatus:
        order_status = self._order_status_repo.get_by_id(order_id)
        order_status.confirm_order()
        updated_order_status = self._order_status_repo.update(order_id, order_status)
        return updated_order_status

    def change_order_status_in_progress(self, order_id: uuid.UUID, payment_status: str) -> OrderStatus:
        order_status = self._order_status_repo.get_by_id(order_id)
        order_status.order_in_progress(payment_status)
        updated_order_status = self._order_status_repo.update(order_id, order_status)
        return updated_order_status

    def change_order_status_ready(self, order_id: uuid.UUID) -> OrderStatus:
        order_status = self._order_status_repo.get_by_id(order_id)
        order_status.order_ready()
        updated_order_status = self._order_status_repo.update(order_id, order_status)
        return updated_order_status

    def change_order_status_finalized(self, order_id: uuid.UUID) -> OrderStatus:
        order_status = self._order_status_repo.get_by_id(order_id)
        order_status.order_finalized()
        updated_order_status = self._order_status_repo.update(order_id, order_status)
        return updated_order_status

    def remove_order(self, order_id: uuid.UUID) -> None:
        self._order_status_repo.remove_order_status(order_id)
