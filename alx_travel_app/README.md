# alx_travel_app
The alxtravelapp project is a real-world Django application that serves as the foundation for a travel listing platform
## 💳 Chapa Payment Integration

This project integrates Chapa API for booking payments.

### 🔧 Setup

- `.env` must contain:


### 🧪 Test Workflow

1. POST `/api/payments/initiate/` with `email`, `amount`, `booking_reference`
2. Use the returned `checkout_url` to make payment.
3. GET `/api/payments/verify/<tx_ref>/` to verify.
4. Status updated in the `Payment` model.
## 📦 Background Task Management with Celery and Email Notifications

### 🎯 Objective
This project uses **Celery** with **RabbitMQ** as the message broker to handle background tasks, and sends email notifications when a booking is created.

---

### ⚙️ Setup Instructions

#### 1. Install Dependencies
Make sure the following are installed:
- RabbitMQ
- Celery
- Required Python packages:

```bash
pip install celery amqp
