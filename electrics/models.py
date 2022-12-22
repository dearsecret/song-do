from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Electric(TimeStampModel):
    custNo = models.CharField(max_length=150)
    bill_ym = models.CharField(max_length=150)
    mr_ymd = models.CharField(max_length=150)
    bill_aply_pwr = models.CharField(max_length=150)
    move_ymd = models.CharField(max_length=150)
    base_bill = models.CharField(max_length=150)
    kwh_bill = models.CharField(max_length=150)
    dc_bill = models.CharField(max_length=150)
    req_bill = models.CharField(max_length=150)
    req_amt = models.CharField(max_length=150)
    lload_usekwh = models.CharField(max_length=150)
    mload_usekwh = models.CharField(max_length=150)
    maxload_usekwh = models.CharField(max_length=150)
    lload_needle = models.CharField(max_length=150)
    mload_needle = models.CharField(max_length=150)
    maxload_needle = models.CharField(max_length=150)
    jn_pwrfact = models.CharField(max_length=150)
    ji_pwrfact = models.CharField(max_length=150)

    def __str__(self):
        return self.bill_ym
