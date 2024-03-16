import datetime
import uuid
from typing import Optional, List

from src.utils.utils import CamelModel


class OrderStatusDTO(CamelModel):
    order_id: uuid.UUID
    creation_date: datetime.datetime
    order_status: str

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
                "creation_date": "2024-01-01T00:05:23",
                "order_status": "Pendente",
            }
        }


class CreateOrderStatusDTO(CamelModel):
    order_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
            }
        }


class UpdateOrderStatusDTO(CamelModel):
    order_id: uuid.UUID
    order_status: str

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
                "order_status": "Pendente",
            }
        }


class RemoveOrderStatusDTO(CamelModel):
    order_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
            }
        }


class OrderStatusDTOResponse(CamelModel):
    result: OrderStatusDTO


class OrderStatusDTOListResponse(CamelModel):
    result: List[OrderStatusDTO]
