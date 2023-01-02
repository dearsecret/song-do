from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Contract(TimeStampModel):
    name = models.CharField(max_length=150)
    start = models.DateField()
    end = models.DateField()

    area = models.IntegerField()
    area_fee = models.IntegerField()
    deposit = models.IntegerField()
    rent = models.IntegerField()

    customer = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.customer.name}"

    class Meta:
        verbose_name = "계약서"
        verbose_name_plural = "계약서"
