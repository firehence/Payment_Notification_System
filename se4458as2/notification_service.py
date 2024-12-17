import pika
import json
import time

RABBITMQ_HOST = 'localhost'
NOTIFICATION_QUEUE = 'notification_queue'


def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection.channel()


def send_notification():
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

    method_frame, header_frame, body = channel.basic_get(queue=NOTIFICATION_QUEUE)
    if method_frame:

        print("The message is being processed, you can check the queue.")
        time.sleep(5)

        notification_data = json.loads(body.decode())
        print(f"Sending notification: {notification_data}")

        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No notification messages in the queue")


if __name__ == "__main__":
    send_notification()
