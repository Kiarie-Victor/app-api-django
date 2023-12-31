import uuid
from django.db import models

class UUIDGenerator(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True