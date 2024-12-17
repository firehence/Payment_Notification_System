import pika
import json
import time

RABBITMQ_HOST = 'localhost'
PAYMENT_QUEUE = 'payment_queue'


def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection.channel()


def process_payment():
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue=PAYMENT_QUEUE, durable=True)

    method_frame, header_frame, body = channel.basic_get(queue=PAYMENT_QUEUE)
    if method_frame:

        print("You can inspect the queue while the message is being processed.")
        time.sleep(5)  # 5 saniye bekle

        payment_data = json.loads(body.decode())
        print(f"Processing payment: {payment_data}")

        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No payment messages in the queue")


if __name__ == "__main__":
    process_payment()
