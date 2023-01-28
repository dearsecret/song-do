from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Notice(TimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    writer = models.ForeignKey(
        "users.User", related_name="memos", on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name_plural = "공지사항 목록"
        verbose_name = "공지사항"


class Memo(TimeStampModel):
    comment = models.CharField(max_length=150, null=True, default=None)
    description = models.CharField(max_length=150, null=True, blank=True)
    bill = models.ForeignKey(
        "bills.bill", related_name="memos", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "알림 목록"
        verbose_name = "알림"
