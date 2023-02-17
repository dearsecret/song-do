from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Promotion(TimeStampModel):
    title = models.CharField(max_length=80)
    thumb = models.URLField()
    description = models.TextField()
    detail = models.TextField(null=True, blank=True)
    category = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "프로모션"
        verbose_name_plural = "행사 목록"
