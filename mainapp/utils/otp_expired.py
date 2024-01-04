from django.utils import timezone

def otp_expired(otp_timestamp):
    if otp_timestamp < timezone.now():
        return True
    return false