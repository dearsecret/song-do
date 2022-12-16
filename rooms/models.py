from django.db import models
from common.models import TimeStampModel

# Create your models here.


class Facility(TimeStampModel):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name


class Kind(TimeStampModel):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Room(TimeStampModel):

    name = models.CharField(max_length=150)
    city = models.CharField(max_length=24)
    address = models.CharField(max_length=250)
    deposit = models.IntegerField()
    price = models.IntegerField()

    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    kind = models.ForeignKey(
        "Kind", related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    descrpiton = models.TextField()
    host = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )

    def __str__(self):
        return f"{self.name} - {self.city}"
