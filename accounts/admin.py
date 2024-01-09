from django.contrib import admin
from accounts.models import Otp, PendingUserModel

# Register your models here.
admin.site.register(Otp)
admin.site.register(PendingUserModel)
