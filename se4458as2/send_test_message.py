import pika
import json

RABBITMQ_HOST = 'localhost'
PAYMENT_QUEUE = 'payment_queue'

def send_test_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=PAYMENT_QUEUE, durable=True)

    message = {
        "user": "aytunyuksek@gmail.com",
        "paymentType": "Credit Card",
        "cardNo": "1234567890123456"
    }

    channel.basic_publish(exchange='',
                          routing_key=PAYMENT_QUEUE,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    print("Test message sent to RabbitMQ!")
    connection.close()

if __name__ == "__main__":
    send_test_message()
