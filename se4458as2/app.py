from flask import Flask, request, jsonify
import pika
import json
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='payment_queue', durable=True)
channel.queue_declare(queue='notification_queue', durable=True)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aytunyuksek48@gmail.com'
app.config['MAIL_PASSWORD'] = 'sjrl qjzi opnz sgnm'
mail = Mail(app)

@app.route('/make-payment', methods=['POST'])
def make_payment():
    try:
        data = request.json
        user = data.get('user')
        payment_type = data.get('paymentType')
        card_no = data.get('cardNo')

        message = json.dumps(data)

        try:
            channel.basic_publish(exchange='',
                                  routing_key='payment_queue',
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,
                                  ))
            print("Mesaj başarıyla gönderildi.")
        except Exception as e:
            print(f"Mesaj gönderme hatası: {e}")
            return jsonify({"error": f"Failed to send message: {str(e)}"}), 500

        return jsonify({"message": "Payment submitted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def process_payment(ch, method, properties, body):
    payment_data = json.loads(body)

    message = json.dumps(payment_data)
    channel.basic_publish(exchange='',
                          routing_key='notification_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    ch.basic_ack(delivery_tag=method.delivery_tag)

def send_email(ch, method, properties, body):
    notification_data = json.loads(body)
    user = notification_data.get('user')
    payment_type = notification_data.get('paymentType')

    if not user or not payment_type:
        print("Missing required data (user or paymentType), email will not be sent.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        with app.app_context():
            msg = Message("Payment Notification",
                          sender="aytunyuksek48@gmail.com",
                          recipients=["aytunyuksek@gmail.com"])
            msg.body = f"Your payment of type {payment_type} has been successfully processed."
            mail.send(msg)

            print(f"Email sent to {user}!")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def start_rabbitmq_consumers():
    channel.basic_consume(queue='payment_queue', on_message_callback=process_payment)
    channel.basic_consume(queue='notification_queue', on_message_callback=send_email)

    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    thread = Thread(target=start_rabbitmq_consumers)
    thread.daemon = True
    thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)
