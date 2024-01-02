from accounts.models import Otp
import random

def otp_generator():
    while True:
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        if not Otp.objects.filter(otp_code=otp).exists():
            break

    return otp

        