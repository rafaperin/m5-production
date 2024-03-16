import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, case
from sqlalchemy.orm import sessionmaker

from src.config.config import settings

from src.entities.models.order_status_entity import order_status_factory, OrderStatus, Status
from src.gateways.orm.order_status_orm import Orders_Status as OrderStatusORM
from src.interfaces.gateways.order_status_gateway_interface import IOrderStatusGateway

connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    connection_uri
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PostgresDBOrderStatusRepository(IOrderStatusGateway):
    @staticmethod
    def to_entity(order_status: OrderStatusORM) -> OrderStatus:
        order_status_entity = order_status_factory(
            order_status.order_id,
            order_status.creation_date,
            order_status.order_status,
        )
        return order_status_entity

    def get_by_id(self, order_id: uuid.UUID) -> Optional[OrderStatus]:
        with SessionLocal() as db:
            order_status_db = db.query(OrderStatusORM).filter(OrderStatusORM.order_id == order_id).first()
        if order_status_db:
            return self.to_entity(order_status_db)  # type: ignore
        else:
            return None

    def get_order_status(self, order_id: uuid.UUID) -> Optional[OrderStatus]:
        with SessionLocal() as db:
            order_status_db = db.query(OrderStatusORM.order_status).filter(OrderStatusORM.order_id == order_id).first()
        if order_status_db:
            return self.to_entity(order_status_db)  # type: ignore
        else:
            return None

    def get_all(self) -> List[OrderStatus]:
        result = []
        with SessionLocal() as db:
            order_status_db = db.query(OrderStatusORM).order_by(OrderStatusORM.creation_date).all()
            if order_status_db:
                for order_status in order_status_db:
                    order_status_entity = self.to_entity(order_status)  # type: ignore
                    result.append(order_status_entity)
        return result

    def list_ongoing_orders(self) -> List[OrderStatus]:
        result = []
        with SessionLocal() as db:
            orders = db.query(OrderStatusORM)\
                .filter(OrderStatusORM.order_status.not_in(['Finalizado', 'Pendente']))\
                .order_by(case(
                        (OrderStatusORM.order_status == Status.READY, 1),  # type: ignore
                        (OrderStatusORM.order_status == Status.IN_PROGRESS, 2),  # type: ignore
                        (OrderStatusORM.order_status == Status.CONFIRMED, 3),  # type: ignore
                        else_=4))\
                .all()

            if orders:
                for order in orders:
                    order_entity = self.to_entity(order)  # type: ignore
                    result.append(order_entity)

        return result

    def create_order_status(self, obj_in: OrderStatus) -> OrderStatus:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = OrderStatusORM(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_order = self.to_entity(db_obj)
        return new_order

    def update(self, order_id: uuid.UUID, obj_in: OrderStatus) -> OrderStatus:
        order_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(OrderStatusORM).filter(OrderStatusORM.order_id == order_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in order_in:
                    setattr(db_obj, field, order_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        updated_order = self.to_entity(db_obj)  # type: ignore
        return updated_order

    def remove_order_status(self, order_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            order = db.query(OrderStatusORM).filter(OrderStatusORM.order_id == order_id).first()
            db.delete(order)
            db.commit()
