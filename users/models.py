from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GENDER_CHOICES(models.TextChoices):
        MALE = "남성", "male"
        FEMALE = "여성", "female"

    name = models.CharField(max_length=150, default="")
    avatar = models.URLField(blank=True)
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    is_host = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES.choices, max_length=6, null=True, blank=True
    )
