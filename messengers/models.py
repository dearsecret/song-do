from django.db import models
from common.models import TimeStampModel
from .phone import send_lms
from .validators import validate_binary_lms, validate_count_lms, validate_binary_subject


# Create your models here.


class SMS(TimeStampModel):
    content = models.CharField(max_length=180)
    to = models.CharField(max_length=12)
    invoice = models.ForeignKey(
        "bills.Invoice",
        related_name="messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "미납요금 SMS 목록"
        verbose_name = "메시지"


class SendLMS(TimeStampModel):
    subject = models.CharField(
        max_length=30,
        validators=[validate_binary_subject],
        help_text="최대 30자",
        verbose_name="제목",
    )
    contents = models.TextField(
        validators=[validate_binary_lms],
        help_text="최대 2000바이트",
        verbose_name="내용",
    )
    phone_number = models.CharField(max_length=12, verbose_name="수신번호")
    sended = models.BooleanField(default=False, editable=False, verbose_name="발신여부")

    created_at = models.DateTimeField(
        auto_now_add=True,
        validators=[validate_count_lms],
        editable=False,
        verbose_name="발송시간",
    )

    def save(self, *args, **kwargs) -> None:
        try:
            send_lms(self.phone_number, subject=self.subject, content=self.contents)
            self.sended = True
            super(SendLMS, self).save(*args, **kwargs)
        except:
            return

    def __str__(self):
        return "메시지"

    class Meta:
        verbose_name_plural = "LMS"
        verbose_name = "메시지 발송"
