from django.db import models
from common.models import TimeStampModel


class WeatherFcst(TimeStampModel):
    baseDate = models.CharField(max_length=8, null=True, blank=True)
    baseTime = models.CharField(max_length=4, null=True, blank=True)
    fcstDate = models.CharField(max_length=8)
    fcstTime = models.CharField(max_length=4)
    LGT = models.CharField(max_length=10, null=True, blank=True)
    PTY = models.CharField(max_length=10, null=True, blank=True)
    RN1 = models.CharField(max_length=10, null=True, blank=True)
    SKY = models.CharField(max_length=10, null=True, blank=True)
    T1H = models.CharField(max_length=10, null=True, blank=True)
    REH = models.CharField(max_length=10, null=True, blank=True)
    UUU = models.CharField(max_length=10, null=True, blank=True)
    VVV = models.CharField(max_length=10, null=True, blank=True)
    VEC = models.CharField(max_length=10, null=True, blank=True)
    WSD = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "날씨"
        verbose_name_plural = "초단기예보"
