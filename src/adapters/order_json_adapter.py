from typing import List

from src.entities.models.order_status_entity import OrderStatus
from src.utils.utils import camelize_dict


def order_status_to_json(order_status: OrderStatus):
    return camelize_dict(order_status.__dict__)


def order_with_qrcode_to_json(order: OrderStatus, qr_code: str):
    order_json = order_status_to_json(order)
    return {"order": order_json, "qrCode": qr_code}


def order_status_list_to_json(order_list: List[OrderStatus]):
    return [order_status_to_json(order) for order in order_list]
