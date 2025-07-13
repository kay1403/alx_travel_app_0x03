from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(to_email, booking_details):
    subject = 'Booking Confirmation'
    message = f'Your booking was successful!\n\nDetails:\n{booking_details}'
    from_email = 'votre.email@gmail.com'
    send_mail(subject, message, from_email, [to_email])
