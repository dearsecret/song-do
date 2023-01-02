from dateutil.relativedelta import relativedelta
from django.db import models
from common.models import TimeStampModel
from contracts.models import Contract
from django.utils import timezone


class Bill(TimeStampModel):
    bill_date = models.DateField(
        default=timezone.now,
        verbose_name="청구일",
    )
    # 상가전체요금
    total = models.PositiveIntegerField(
        verbose_name="총청구금액",
        help_text="상가 전체에 해당하는 전기료 청구금액의 합계",
    )
    maintanance = models.PositiveIntegerField(
        verbose_name="관리실금액",
        help_text="상가 관리단 전기료의 합계",
    )

    # 층별요금
    floor = models.PositiveIntegerField(
        verbose_name="한전 청구요금", help_text="부가세가 포함된 4층 전기료 청구요금"
    )
    basic = models.PositiveIntegerField(
        default=0, verbose_name="한전 기본요금", help_text="적용요금에 따른 기본 요금"
    )
    usage = models.PositiveIntegerField(
        blank=True, verbose_name="당월 사용량(kw)", help_text="청구서에 기재된 전력사용량"
    )
    area_cnt = models.PositiveIntegerField(default=0)
    area_sum = models.PositiveIntegerField(default=0, blank=True, verbose_name="해당층 면적")

    def start_date(self):
        return self.bill_date + relativedelta(months=-1, days=1)

    def public_share(self):
        # 공용 전기료 - 기본 지분율 계산
        return self.maintanance * 0.4 * 0.15

    def public_usage(self):
        # 공용 전기료 - 전기 사용료 계산
        return (self.maintanance * 0.6) * (self.floor / self.total)

    def total_public(self):
        # 공용 - 공용 전기료 합산
        return self.public_share() + self.public_usage()

    def none_tax(self):
        # 4층 세전 전력사용료 계산
        if self.floor and self.basic:
            return (self.floor - self.basic * 1.1) / 1.1

    def usage_sum(self):
        # 각호실 사용량 계산
        sum = 0
        for invoice in self.invoices.all():
            if invoice.usage:
                sum += invoice.usage
        return sum

    def unit_price(self):
        # 전력 단가 계산
        if self.none_tax() and self.usage:
            return self.none_tax() / self.usage

    def ratio(self):
        # 소실율 계산
        if self.usage_sum():
            return self.usage / self.usage_sum()

    def save(self, **kwargs):
        sum = 0
        for contract in Contract.objects.filter(
            end__gte=self.start_date(),
            start__lte=self.start_date(),
        ):
            sum += contract.area
            invoices = Invoice.objects.filter(
                bill=self,
                contract=contract,
            )
            if not invoices:
                Invoice(
                    bill=self,
                    contract=contract,
                ).save()
            else:
                invoices.update(
                    bill=self,
                    contract=contract,
                )
        self.area_sum = sum
        super().save(**kwargs)

    def __str__(self):
        prev_month = self.start_date()
        return f"{prev_month.strftime('%Y년 %m월 이용내역')}"

    public_share.short_description = "공용기본전기료"
    public_usage.short_description = "공용누적전기료"
    total_public.short_description = "총공용전기료"
    none_tax.short_description = "부가세전 청구금"
    start_date.short_description = "시작일"
    unit_price.short_description = "전력단위당 단가"
    usage_sum.short_description = "사용량 총합"
    ratio.short_description = "소실율"

    class Meta:
        verbose_name = "청구서"
        verbose_name_plural = "1. 청구서 입력"


class Invoice(TimeStampModel):
    is_issue = models.BooleanField(verbose_name="발행여부", default=False)
    usage = models.PositiveIntegerField(
        verbose_name="호실별 사용량",
        help_text="호실별 검침량",
        blank=True,
        null=True,
    )
    contract = models.ForeignKey(
        "contracts.contract",
        related_name="invoices",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="계약자 정보",
    )
    bill = models.ForeignKey(
        "bills.Bill",
        related_name="invoices",
        on_delete=models.CASCADE,
        verbose_name="당월 청구서 정보",
    )

    def usage_ratio(self):
        if self.usage:
            return f"{round(self.usage / self.bill.usage_sum()*100,3)}%"

    def basic(self):
        return int(self.bill.basic * self.contract.area / (self.bill.area_sum))

    def add_unit(self):
        if self.bill.unit_price() and self.usage:
            return int(self.bill.unit_price() * self.usage)

    def without_tax(self):
        if (self.usage) and self.bill.unit_price():
            return int(
                self.bill.unit_price() * self.usage
                + int(self.bill.basic * (self.contract.area / self.bill.area_sum))
            )

    def tax(self):
        if (self.usage) and self.bill.unit_price():
            return int(self.without_tax() * 0.1)

    def add_tax(self):
        if self.usage:
            # + self.bill.basic * (self.contract.area / self.bill.area_sum)
            return int(self.without_tax() * 1.1)

    def public_share(self):
        return int(self.bill.public_share() * (self.contract.area / self.bill.area_sum))

    def public_usage(self):
        return int((self.usage / self.bill.usage_sum() * self.bill.public_usage()))

    def public(self):
        return self.public_usage() + self.public_share()

    def area_fee(self):
        if self.contract:
            something = self.contract.area * self.contract.area_fee
            return something

    def total(self):
        if self.add_tax() and self.public():
            return int(self.add_tax() + self.area_fee() + self.public())

    def __str__(self):
        if self.contract:
            return self.contract.name
        else:
            return self.bill

    class Meta:
        verbose_name = "인보이스"
        verbose_name_plural = "2. 인보이스"

    public_share.short_descripiton = "공용 기본전기료"
    public_usage.short_descripiton = "공용 전기사용료"
    area_fee.short_description = "기본관리비"
    usage_ratio.short_description = "사용 비율"
    add_tax.short_description = "부가세 가산"
    total.short_description = "청구요금"
