from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


def validate_binary_lms(content):
    if len(content.encode("utf-8")) > 2000:
        raise ValidationError(
            _(" 바이트 초과"),
            params={"content": content},
        )


def validate_binary_subject(subject):
    print(len(subject.encode("utf-8")))
    if len(subject.encode("utf-8")) > 40:
        raise ValidationError(
            _(" 바이트 초과"),
            params={"subject": subject},
        )


def validate_count_lms(self, value):
    if self.objects.filter(create_at__gte=value - timedelta(days=30)).count() > 10:
        raise ValidationError(
            _("%(value) 30건 초과"),
            params={"vaue": value},
        )
