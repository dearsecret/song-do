from django.db import models
from common.models import TimeStampModel


class Customer(TimeStampModel):
    title = models.CharField(max_length=12, verbose_name="구분")
    custNum = models.CharField(max_length=10, verbose_name="고객번호")
    description = models.TextField(null=True, blank=True, verbose_name="비고")

    def __str__(self):
        return f"{self.title} - {self.custNum}"

    class Meta:
        verbose_name = "고객번호"
        verbose_name_plural = "고객번호 목록"


class Billing(TimeStampModel):
    custNo = models.ForeignKey(
        "informations.Customer",
        related_name="billings",
        on_delete=models.CASCADE,
        verbose_name="고객번호",
    )
    bill_ym = models.CharField(max_length=6, verbose_name="청구년월")
    mr_ymd = models.CharField(max_length=2, verbose_name="정기검침일")
    bill_aply_pwr = models.CharField(max_length=15, verbose_name="요금적용전력")
    move_ymd = models.CharField(max_length=8, verbose_name="이사정산일")
    base_bill = models.CharField(max_length=17, verbose_name="기본요금")
    kwh_bill = models.CharField(max_length=17, verbose_name="전력량요금")
    dc_bill = models.CharField(max_length=15, verbose_name="할인")
    req_bill = models.CharField(max_length=15, verbose_name="전기요금계")
    req_amt = models.CharField(max_length=15, verbose_name="청구요금")
    lload_usekwh = models.CharField(max_length=15, verbose_name="경부하사용량")
    mload_usekwh = models.CharField(max_length=15, verbose_name="중부하사용량")
    maxload_usekwh = models.CharField(max_length=15, verbose_name="최대부하사용량")
    lload_needle = models.CharField(max_length=15, verbose_name="경부하당월지침")
    mload_needle = models.CharField(max_length=15, verbose_name="중부하당월지침")
    maxload_needle = models.CharField(max_length=15, verbose_name="최대부하당월지침")
    jn_pwrfact = models.CharField(max_length=6, verbose_name="진상역률")
    ji_pwrfact = models.CharField(max_length=6, verbose_name="지상역률")

    def __str__(self):
        return f"{self.bill_ym} - {self.custNo.title}"

    class Meta:
        verbose_name = "청구정보"
        verbose_name_plural = "고객청구정보 목록"


class Accounting(TimeStampModel):
    class CountKind(models.TextChoices):
        DEPOSIT = ("deposit", "입금")
        WITHDRAWAL = ("withdrawal", "출금")

    name = models.CharField(max_length=120)
    price = models.IntegerField()
    description = models.TextField(max_length=200, null=True, blank=True)
    kind = models.CharField(
        max_length=10,
        choices=CountKind.choices,
    )
    date = models.DateField()

    class Meta:
        verbose_name = "회계내역"
        verbose_name_plural = "회계내역 목록"
