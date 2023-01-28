from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Contract(TimeStampModel):
    name = models.CharField(max_length=150, verbose_name="호실")
    start = models.DateField(verbose_name="시작일")
    end = models.DateField(verbose_name="종료일")

    area = models.IntegerField(verbose_name="평형")
    area_fee = models.IntegerField(verbose_name="평당 관리비")
    deposit = models.IntegerField(verbose_name="보증금")
    rent = models.IntegerField(verbose_name="월세")

    customer = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="계약자 정보",
    )

    def __str__(self):
        return f"{self.name} - {self.customer.name}"

    class Meta:
        verbose_name = "계약서"
        verbose_name_plural = "계약서"
