from django.db import models
from common.models import TimeStampModel

# Create your models here.


class SMS(TimeStampModel):
    content = models.CharField(max_length=180)
    to = models.CharField(max_length=12)
    invoice = models.ForeignKey(
        "bills.Invoice",
        related_name="messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "SMS"
        verbose_name = "메시지"
