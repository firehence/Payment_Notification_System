# Payment Notification System with RabbitMQ, Flask and Flask-Mail

This project implements a payment notification system using RabbitMQ, Flask (a Python web framework), and Flask-Mail to simulate a real-world asynchronous messaging system. The goal is to process payments, send notifications, and notify users about the status of their payments via email.

## Project Overview

The application uses RabbitMQ to handle message queues for different stages of the process:

#### payment_queue: Handles incoming payment requests for processing.
#### notification_queue: Sends email notifications to users about their payment status.

### Tech Stack
Python
Flask (Web Framework)
RabbitMQ (Message Broker)
Flask-Mail (Email Sending Service)
JSON (Data format)

### Installation and Setup
### 1. Install Python
Ensure that you have Python installed. If not, you can download it from Python Official Website.

### 2. Install Required Python Packages
You need the following Python packages for the project. You can install them using pip:
  pip install pika Flask Flask-Mail

### 3. Install RabbitMQ
Install RabbitMQ and set it up on your system. Follow the instructions in the RabbitMQ Installation Guide to install and configure RabbitMQ.

### 4. Set Up Gmail SMTP for Sending Emails
In order to send email notifications via Gmail, you'll need to set up Flask-Mail to work with Gmail's SMTP server. Use your Gmail credentials or create an app-specific password.

Set up your Gmail SMTP credentials in your app.config:
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your password

## How It Works
### Payment Request Handling
The Flask application exposes an endpoint POST /make-payment that accepts payment data in JSON format. When a payment request is made, the data is sent to the payment_queue in RabbitMQ for further processing.

### Processing Payments
Once a message is added to the payment_queue, the system processes the payment by consuming the message from the queue and acknowledging the message with channel.basic_ack().

### Sending Notifications
After processing a payment, the data is forwarded to the notification_queue. The send_email function listens for messages on this queue and sends an email notification to the user using Flask-Mail.

### Email Notification
After the payment is processed successfully, an email notification is sent to the user confirming their payment details.

### Running the Application

### 1. Start RabbitMQ
Ensure that RabbitMQ is running on your machine. You can start it by using:
rabbitmq-server start

### 2. Run the Flask Application
Once RabbitMQ is running, you can start the Flask application by running the following command:
python app.py
This will start the Flask server and expose the /make-payment endpoint. You can test the endpoint by sending a POST request to http://localhost:5000/make-payment.

### Test the Payment System
### 1. Sending a Payment Request
You can send a test payment request using a tool like Postman. Here is an example POST request:

URL: http://localhost:5000/make-payment

Body (JSON):
{
    "user": "test-user@example.com",
    "paymentType": "Credit Card",
    "cardNo": "1234567890123456"
}

### 2. Observe the RabbitMQ Queues
Once a payment request is processed, you can observe the payment_queue and notification_queue in the RabbitMQ Management Interface at http://localhost:15672 (default login: guest / guest). You should see the messages in the respective queues.

### 3. Check for Email Notification
After processing the payment, an email notification will be sent to the user’s email address provided in the request. Check the inbox of the provided email address for a payment confirmation email.

## Conclusion
This system simulates a payment processing and notification system using RabbitMQ for message queuing and Flask-Mail for email notifications. It's designed to handle asynchronous operations like processing payments and notifying users without blocking the main application flow.
   
