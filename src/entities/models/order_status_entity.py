import datetime
import uuid
from dataclasses import dataclass
from typing import List

from src.entities.errors.order_status_error import OrderStatusError


class Status:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    IN_PROGRESS = "Em preparo"
    READY = "Pronto"
    FINALIZED = "Finalizado"


class PaymentStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    REFUSED = "Negado"


@dataclass
class OrderStatus:
    order_id: uuid.UUID
    creation_date: datetime.datetime
    order_status: str

    @classmethod
    def create_new_order_status(cls, order_id: uuid.uuid4()) -> "OrderStatus":
        return cls(
            order_id,
            datetime.datetime.utcnow(),
            Status.PENDING
        )

    def check_if_pending_order(self) -> None:
        if self.order_status != Status.PENDING:
            raise OrderStatusError("Order already confirmed, modification not allowed!")

    @staticmethod
    def check_payment_status(payment_status: str) -> None:
        if payment_status == PaymentStatus.PENDING:
            raise OrderStatusError("Order payment id pending!")
        if payment_status == PaymentStatus.REFUSED:
            raise OrderStatusError("Order payment was refused! Please contact your payment provider.")

    def confirm_order(self) -> None:
        self.check_if_pending_order()
        self.order_status = Status.CONFIRMED

    def order_in_progress(self, payment_status: str) -> None:
        if self.order_status == Status.CONFIRMED:
            self.check_payment_status(payment_status)
            self.order_status = Status.IN_PROGRESS
        elif self.order_status == Status.PENDING:
            raise OrderStatusError("Order not yet confirmed!")
        else:
            raise OrderStatusError("Order already in progress!")

    def order_ready(self) -> None:
        if self.order_status == Status.IN_PROGRESS:
            self.order_status = Status.READY
        elif self.order_status == Status.CONFIRMED or self.order_status == Status.PENDING:
            raise OrderStatusError("Order not yet in progress!")
        else:
            raise OrderStatusError("Order already ready!")

    def order_finalized(self) -> None:
        if self.order_status == Status.READY:
            self.order_status = Status.FINALIZED
        else:
            raise OrderStatusError("Order not yet ready!")


def order_status_factory(
    order_id: uuid.UUID,
    creation_date: datetime.datetime,
    order_status: str
) -> OrderStatus:
    return OrderStatus(
        order_id=order_id,
        creation_date=creation_date,
        order_status=order_status
    )
