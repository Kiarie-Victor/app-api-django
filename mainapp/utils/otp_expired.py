from django.utils import timezone

def otp_expired(otp_timestamp : timezone):
    expire_time = otp_timestamp + timezone.timedelta(minutes=3)
    if expire_time < timezone.now():
        return True
    return false