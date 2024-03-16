import uuid

from fastapi import APIRouter

from src.adapters.order_json_adapter import order_status_list_to_json, order_status_to_json, order_with_qrcode_to_json
from src.config.errors import RepositoryError, ResourceNotFound, DomainError
from src.entities.errors.order_status_error import OrderStatusError
from src.entities.schemas.order_status_dto import CreateOrderStatusDTO
from src.gateways.postgres_gateways.order_status_gateway import PostgresDBOrderStatusRepository
from src.usecases.order_status_usecase import OrderStatusUseCase

router = APIRouter()


class OrderStatusController:
    @staticmethod
    async def get_all_orders_status() -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            all_orders = OrderStatusUseCase(order_status_gateway).get_all()
            result = order_status_list_to_json(all_orders)
        except Exception as e:
            print(e)
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def list_ongoing_orders() -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            ongoing_orders = OrderStatusUseCase(order_status_gateway).list_ongoing_orders()
            result = order_status_list_to_json(ongoing_orders)
        except Exception as e:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_order_by_id(
            order_id: uuid.UUID
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).get_by_id(order_id)
            result = order_status_to_json(order)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_order_status(
        order_id: uuid.UUID
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).get_order_status(order_id)
            result = order_status_to_json(order)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_order(
        request: CreateOrderStatusDTO
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).create_order_status(request)
            result = order_status_to_json(order)
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def confirm_order(
        order_id: uuid.UUID,
        qr_code: str
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).confirm_order(order_id)
            result = order_with_qrcode_to_json(order, qr_code)
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    def change_order_status_in_progress(
        order_id: uuid.UUID,
        payment_status: str
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).change_order_status_in_progress(order_id, payment_status)
            result = order_status_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_status_ready(
        order_id: uuid.UUID
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).change_order_status_ready(order_id)
            result = order_status_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_order_status_finalized(
        order_id: uuid.UUID
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            order = OrderStatusUseCase(order_status_gateway).change_order_status_finalized(order_id)
            result = order_status_to_json(order)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_order_status(
        order_id: uuid.UUID
    ) -> dict:
        order_status_gateway = PostgresDBOrderStatusRepository()

        try:
            OrderStatusUseCase(order_status_gateway).remove_order_status(order_id)
        except DomainError:
            raise OrderStatusError.invalid_status()
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Order removed successfully"}
