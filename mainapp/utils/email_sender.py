from django.core.mail import EmailMessage
from decouple import config

def sendEmail(username, otp_code, email) -> bool:
    receiver = email
    subject = f'Otp Verification {otp_code}'
    sender = config('EMAIL_HOST_USER')
    message = f"Dear {username}, \n Your code is: {otp_code}. \n Use it to access your access account. If you didn't request this, simply ignore this message.\n Yours, \n Anonymous"

    try:
        email = EmailMessage(subject = subject, body = message, from_email = sender, to = [receiver])
        email.send(fail_silently=False)
        return True

    except Exception as e:
        return False