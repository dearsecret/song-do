from django.utils import timezone
from django.db import transaction
from django.conf import settings
import requests
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from realtimes.models import WeatherFcst


def get_forecast():
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    now = timezone.localtime(timezone.now())
    if now.minute < 45:
        now = now + timedelta(minutes=-45)

    base_date = now.strftime("%Y%m%d")
    # 매시각 30분에 생성되고 45분 이후에 호출 가능
    # 1000번 호출 가능하여, 데이터베이스 업데이트를 통해 안정적인 api 제공을 목적으로함
    # 하루 24*60//10 = 144번 업데이트
    # 개발모드에서는 reload 하므로 , python manage.py runserver --noreload
    base_time = now.strftime("%H") + "30"
    params = {
        "numOfRows": "60",
        "pageNo": "1",
        "base_date": base_date,
        "base_time": base_time,
        "nx": "54",
        "ny": "123",
        "dataType": "JSON",
        "serviceKey": settings.FORECAST_KEY,
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        res = res.json()
        try:
            fcsts = res.get("response").get("body").get("items").get("item")
            with transaction.atomic():
                for i in fcsts:
                    new_value = {i.get("category"): i.get("fcstValue")}
                    WeatherFcst.objects.update_or_create(
                        fcstDate=i.get("fcstDate"),
                        fcstTime=i.get("fcstTime"),
                        defaults=new_value,
                    )
                expired = WeatherFcst.objects.filter(updated_at__lt=now)
                if expired.exists():
                    expired.delete()
        except:
            pass


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(
        get_forecast,
        "cron",
        minute="45",
        id="forecast",
    )
    scheduler.start()
