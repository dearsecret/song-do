from django.contrib import admin
from .models import WeatherFcst


@admin.register(WeatherFcst)
class ForecastAdmin(admin.ModelAdmin):
    list_display = (
        "fcstDate",
        "fcstTime",
        "LGT",
        "PTY",
        "RN1",
        "SKY",
        "T1H",
        "REH",
        "UUU",
        "VVV",
        "VEC",
        "WSD",
    )
