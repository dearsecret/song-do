from dateutil.relativedelta import relativedelta
from django.db import models
from common.models import TimeStampModel
from contracts.models import Contract
from django.utils import timezone
from notices.models import Memo


class Bill(TimeStampModel):
    is_issue = models.BooleanField(default=False, verbose_name="발행여부")
    ratio = models.FloatField(null=True, verbose_name="소실율", help_text="발행시 계산합니다.")
    start_date = models.DateField(verbose_name="시작일")
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
        verbose_name="한전 기본요금", help_text="적용요금에 따른 기본 요금"
    )
    usage = models.PositiveIntegerField(
        blank=True, verbose_name="당월 사용량(kw)", help_text="청구서에 기재된 전력사용량"
    )
    usage_sum = models.PositiveIntegerField(null=True, verbose_name="사용자 검침량 총합")
    area_sum = models.PositiveIntegerField(verbose_name="임대면적 합계")
    public_share = models.PositiveIntegerField(verbose_name="공용 기본전기료")
    public_usage = models.PositiveIntegerField(verbose_name="공용 사용전기료")
    total_public = models.PositiveIntegerField(verbose_name="공용전기료 총합")
    none_tax = models.PositiveIntegerField(verbose_name="세전 사용량 전기료")
    unit_price = models.PositiveIntegerField(verbose_name="단위당 단가")

    owner_charge = models.ManyToManyField(
        "bills.OwnerCharge",
        related_name="bills",
        blank=True,
        verbose_name="임대인 부담",
    )

    def get_start_date(self):
        return self.bill_date + relativedelta(months=-1, days=1)

    def get_public_share(self):
        # 기본 지분율 계산
        return round(self.maintanance * 0.4 * 0.15, 0)

    def get_public_usage(self):
        # 전기 사용료 계산
        return int(((self.maintanance * 0.6) / self.total) * self.floor)

    def get_total_public(self):
        # 공용 - 공용 전기료 합산
        return self.get_public_share() + self.get_public_usage()

    def get_none_tax(self):
        # 4층 세전 전력사용료 계산
        if (self.floor - self.basic * 1.1) / 1.1 > 0:
            return int((self.floor - self.basic * 1.1) / 1.1)
        return 0

    def get_unit_price(self):
        # 전력 단가 계산
        return self.none_tax / self.usage

    def get_ratio(self):
        return self.usage / self.get_usage_sum()

    # -----하단부 반드시 메서드로 할 것------
    def get_usage_sum(self):
        # 각호실 사용량 계산
        if self.invoices.all():
            sum = 0
            for invoice in self.invoices.all():
                if invoice.usage:
                    sum += invoice.usage
            return sum

    def is_ready(self):
        if self.pk:
            if self.invoices:
                if None in [invoice.usage for invoice in self.invoices.all()]:
                    return False
                else:
                    return True

    # -------------------------------
    def valid_contracts(self):
        contracts = Contract.objects.filter(
            end__gte=self.get_start_date(),
            start__lte=self.get_start_date(),
        ).all()
        return contracts

    def area_summation(self):
        sum = 0
        contracts = self.valid_contracts()
        if contracts:
            for contract in contracts.all():
                sum += contract.area
            return sum
        return 0

    def save(self, *arg, **kwargs):
        if self.pk:
            if not self.is_issue:
                self.usage_sum = None
                self.ratio = None
            elif not self.is_ready():
                self.is_issue = False
                self.usage_sum = None
                self.ratio = None
            else:
                self.usage_sum = self.get_usage_sum()
                self.ratio = self.get_ratio()
        else:
            self.is_issue = False
        self.start_date = self.get_start_date()
        self.public_share = self.get_public_share()
        self.public_usage = self.get_public_usage()
        self.total_public = self.get_total_public()
        self.area_sum = self.area_summation()
        self.none_tax = self.get_none_tax()
        self.unit_price = self.get_unit_price()
        super(Bill, self).save(*arg, **kwargs)

        contracts = self.valid_contracts()
        for contract in contracts:
            Invoice.objects.update_or_create(
                bill=self,
                contract=contract,
            )

    def __str__(self):
        prev_month = self.start_date
        return f"{prev_month.strftime('%Y년 %m월 이용내역')}"

    usage_sum.short_description = "사용량 총합"

    class Meta:
        verbose_name = "청구서"
        verbose_name_plural = "1. 청구서 입력"


class Invoice(TimeStampModel):
    is_payed = models.BooleanField(verbose_name="입금여부", default=False)
    usage = models.PositiveIntegerField(
        verbose_name="검침량",
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

    public_share = models.PositiveIntegerField(verbose_name="공용 기본전기료")
    area_fee = models.PositiveIntegerField(verbose_name="기본관리비")
    basic = models.PositiveIntegerField(verbose_name="기본전기료")
    ratio_usage = models.PositiveIntegerField(null=True, verbose_name="전력사용량")
    add_unit = models.PositiveIntegerField(null=True, verbose_name="전력사용요금")
    without_tax = models.PositiveIntegerField(null=True, verbose_name="전기요금")
    tax = models.PositiveIntegerField(null=True, verbose_name="부가세")
    add_tax = models.PositiveIntegerField(null=True, verbose_name="사용자 합계")
    public_usage = models.PositiveIntegerField(null=True, verbose_name="공용 전력사용요금")
    public = models.PositiveIntegerField(null=True, verbose_name="공용 합계")
    total = models.PositiveIntegerField(null=True, verbose_name="총합")

    def get_basic(self):
        return int(self.bill.basic * (self.contract.area / self.bill.area_sum))

    def get_public_share(self):
        return int(self.bill.public_share * (self.contract.area / self.bill.area_sum))

    def get_area_fee(self):
        return int(self.contract.area * self.contract.area_fee)

    def get_ratio_usage(self):
        try:
            return int(self.bill.ratio * self.usage)
        except:
            return None

    def get_add_unit(self):
        try:
            return int(self.bill.unit_price * self.ratio_usage)
        except:
            return None

    def get_without_tax(self):
        try:
            return int(self.add_unit + self.get_basic())
        except:
            return None

    def get_tax(self):
        try:
            return int(self.without_tax * 0.1)
        except:
            return None

    def get_add_tax(self):
        if self.without_tax:
            return int(self.without_tax + self.tax)

    # 메서드 필드

    def get_public_usage(self):
        try:
            return int((self.usage / self.bill.usage_sum) * self.bill.public_usage)
        except:
            return None

    def get_public(self):
        try:
            return int(self.public_usage + self.public_share)
        except:
            return None

    def get_total(self):
        try:
            return int(self.add_tax + self.area_fee + self.public)
        except:
            return None

    def save(self, *arg, **kwargs):
        self.basic = self.get_basic()
        self.public_share = self.get_public_share()
        self.area_fee = self.get_area_fee()
        if self.bill.ratio:
            self.ratio_usage = self.get_ratio_usage()
            self.add_unit = self.get_add_unit()
            self.without_tax = self.get_without_tax()
            self.tax = self.get_tax()
            self.add_tax = self.get_add_tax()
            self.public_usage = self.get_public_usage()
            self.public = self.get_public()
            self.total = self.get_total()
        else:
            self.ratio_usage = None
            self.add_unit = None
            self.without_tax = None
            self.tax = None
            self.add_tax = None
            self.public_usage = None
            self.public = None
            self.total = None
        super(Invoice, self).save(*arg, **kwargs)

        if self.bill.is_issue:
            if self.bill.get_usage_sum() != self.bill.usage_sum:
                self.bill.is_issue = False
                self.bill.save()

    def __str__(self):
        if self.contract:
            return self.contract.name
        else:
            return self.bill

    class Meta:
        verbose_name = "인보이스"
        verbose_name_plural = "2. 인보이스"


class OwnerCharge(TimeStampModel):
    title = models.CharField(max_length=50, verbose_name="항목")
    charge = models.IntegerField(verbose_name="비용")

    class Meta:
        verbose_name = "부담내역"
        verbose_name_plural = "임대인 부담"

    def __str__(self):
        return self.title
