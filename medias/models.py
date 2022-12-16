from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Photo(TimeStampModel):
    url = models.URLField()
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="photos",
        null=True,
        blank=True,
    )
