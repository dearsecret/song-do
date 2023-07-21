from django.db import models
from django.utils import timezone
from common.models import TimeStampModel
from dateutil.relativedelta import relativedelta
from .calculators import count_month

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

    def save(self, *arg, **kwargs):
        # n = count_month(self.start, self.end)
        # for i in range(n):
        #     if self.start.day > 28:
        #         end = self.start.replace(day=1) + relativedelta(months=i + 2, days=-1)
        #     else:
        #         end = self.start + relativedelta(months=i + 1, days=-1)
        #     if not (
        #         Rent.objects.filter(payed_cnt=i + 1, contract=self).exists()
        #         or timezone.localtime(timezone.now()).date() > end
        #     ):
        #         Rent(payed_cnt=i + 1, usage_end=end, contract=self).save()
        super(Contract, self).save(*arg, **kwargs)


class Rent(TimeStampModel):
    payed_cnt = models.PositiveIntegerField(verbose_name="회차")
    usage_end = models.DateField(verbose_name="납기일")
    check_date = models.DateField(null=True, blank=True)
    contract = models.ForeignKey(
        "contracts.Contract",
        related_name="rents",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="계약서",
    )

    def get_is_payed(self):
        if self.check_date:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.payed_cnt}회"

    class Meta:
        verbose_name = "납부회차"
        verbose_name_plural = "월납입금 목록"
