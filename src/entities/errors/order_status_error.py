from src.config.errors import DomainError


class OrderStatusError(DomainError):
    @classmethod
    def invalid_status(cls) -> "OrderStatusError":
        return cls("Provided order status is not valid!")
