import json
import uuid

import httpx
from fastapi import APIRouter, status

from src.api.errors.api_errors import APIErrorMessage
from src.config.config import Settings, settings
from src.config.errors import RepositoryError, ResourceNotFound, DomainError
from src.controllers.order_status_controller import OrderStatusController
from src.entities.errors.order_status_error import OrderStatusError
from src.entities.schemas.order_status_dto import OrderStatusDTOListResponse, OrderStatusDTOResponse, \
    CreateOrderStatusDTO
from src.external.messaging_client import MessagingClient

router = APIRouter()


@router.get(
    "/order-status", tags=["Order Status"],
    response_model=OrderStatusDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_orders_status() -> dict:
    try:
        result = await OrderStatusController.get_all_orders_status()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/order-status/ongoing", tags=["Order Status"],
    response_model=OrderStatusDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def list_ongoing_orders() -> dict:
    try:
        result = await OrderStatusController.list_ongoing_orders()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/order-status/id/{order_id}", tags=["Order Status"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_order_by_id(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderStatusController.get_order_by_id(order_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/order-status/id/{order_id}/status", tags=["Order Status"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_order_status(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderStatusController.get_order_by_id(order_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No order with id: {order_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/order-status",  tags=["Orders"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_order_status(
    request: CreateOrderStatusDTO
) -> dict:
    try:
        result = await OrderStatusController.create_order(request)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/order-status/{order_id}/checkout", tags=["Order Status"],
    # response_model=OrderWithQrCodeDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def confirm_order(
    order_id: uuid.UUID
) -> dict:
    try:
        headers = {
            # "Authorization": f"Bearer {access_token}",
        }

        params = {
            "order_id": str(order_id)
        }

        r = httpx.post(f"{settings.PAYMENTS_SERVICE}/payments/mercado-pago", headers=headers, json=params)
        json_response = json.loads(r.content)
        qr_code = json_response["result"]["qrCode"]

        print(r)

        result = await OrderStatusController.confirm_order(order_id, qr_code)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/order-status/{order_id}/in-progress", tags=["Order Status"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_in_progress(
    order_id: uuid.UUID
) -> dict:
    try:
        headers = {
            # "Authorization": f"Bearer {access_token}",
        }

        r = httpx.get(f"{settings.PAYMENTS_SERVICE}/payments/id/{order_id}", headers=headers)
        json_response = json.loads(r.content)
        payment_status = json_response["result"]["paymentStatus"]

        result = await OrderStatusController.change_order_status_in_progress(order_id, payment_status)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/order-status/{order_id}/ready", tags=["Order Status"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_ready(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderStatusController.change_order_status_ready(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/order-status/{order_id}/finalized", tags=["Order Status"],
    response_model=OrderStatusDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def order_finalized(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await OrderStatusController.change_order_status_finalized(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/order-status/{order_id}", tags=["Order Status"],
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_order_status(
    order_id: uuid.UUID
) -> dict:
    try:
        await OrderStatusController.remove_order_status(order_id)
    except DomainError:
        raise OrderStatusError.invalid_status()
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Order status removed successfully"}
