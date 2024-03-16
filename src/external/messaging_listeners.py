import json
import threading
import time

import httpx

from src.config.config import settings

from src.controllers.order_status_controller import OrderStatusController
from src.external.messaging_client import MessagingClient, sqs_client


class PaymentConfirmationListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = settings.PAYMENT_CONFIRMATION_QUEUE
        self.shutdown_flag = threading.Event()

    def run(self, *args, **kwargs):
        while not self.shutdown_flag.is_set():
            message = MessagingClient().receive(self.queue)
            if message is not None:
                try:
                    receipt_handle = message['ReceiptHandle']
                    message_body = json.loads(message["Body"])
                    content = json.loads(message_body["Message"])

                    OrderStatusController.change_order_status_in_progress(
                        content["order_id"], content["payment_status"]
                    )

                    sqs_client.delete_message(
                        QueueUrl=self.queue,
                        ReceiptHandle=receipt_handle
                    )

                    order_id = content["order_id"]

                    r = httpx.get(f"{settings.ORDERS_SERVICE}/orders/id/{order_id}")
                    json_response = json.loads(r.content)

                    customer_id = json_response["result"]["customerId"]

                    r = httpx.get(f"{settings.CUSTOMERS_SERVICE}/customers/id/{customer_id}")
                    json_response = json.loads(r.content)

                    message = f"O pagamento do pedido {order_id} foi confirmado e o mesmo está sendo produzido"

                    MessagingClient.send_sms(json_response["result"]["phone"], message)

                    time.sleep(5)
                except Exception as e:
                    print(e)

            print("payment confirmation listener running")


class PaymentErrorListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = settings.PAYMENT_ERROR_QUEUE
        self.shutdown_flag = threading.Event()

    def run(self, *args, **kwargs):
        while not self.shutdown_flag.is_set():
            message = MessagingClient().receive(self.queue)
            if message is not None:
                receipt_handle = message['ReceiptHandle']
                message_body = json.loads(message["Body"])
                content = json.loads(message_body["Message"])

                order_id = content["order_id"]

                r = httpx.get(f"{settings.ORDERS_SERVICE}/orders/id/{order_id}")
                json_response = json.loads(r.content)

                customer_id = json_response["result"]["customerId"]

                r = httpx.get(f"{settings.CUSTOMERS_SERVICE}/customers/id/{customer_id}")
                json_response = json.loads(r.content)

                notification = {
                    "order_id": order_id,
                    "message": "Houve um erro ao processar o pagamento, tente novamente"
                }

                MessagingClient.send_sms(json_response["result"]["phone"], notification)

                sqs_client.delete_message(
                    QueueUrl=self.queue,
                    ReceiptHandle=receipt_handle
                )
            time.sleep(5)
            print("payment error listener running")
