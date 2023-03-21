from django.utils import timezone
from django.db import transaction
from django.conf import settings
import requests
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from realtimes.models import WeatherFcst
from bills.models import Invoice
from messengers.phone import send_sms
from messengers.models import SMS


def get_forecast():
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    now = timezone.localtime(timezone.now())
    if now.minute < 45:
        now = now + timedelta(minutes=-45)

    base_date = now.strftime("%Y%m%d")
    # 매시각 30분에 생성되고 45분 이후에 호출 가능
    # 1000번 호출 가능하여, 데이터베이스 업데이트를 통해 안정적인 api 제공을 목적으로함
    # (하루 24*60//10 = 144번 업데이트 | 매시각 45분마다 = 24번 업데이트)
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


def check_unbilled():
    # 매월 9일 실행할 것
    try:
        # 청구서 발급 후 7일 경과, 미납내역 필터링
        invoices = Invoice.objects.filter(
            bill__is_issue=True,
            is_payed=False,
            # updated_at__range=[
            #     timezone.now() + timedelta(days=-8),
            #     timezone.now() + timedelta(days=-7),
            # ],
        )
        if invoices.exists():
            sent_lst = []
            for invoice in invoices:
                if not SMS.objects.filter(invoice=invoice).exists():
                    if (
                        not SMS.objects.filter(
                            created_at__gte=timezone.localtime(timezone.now()).date()
                            + timedelta(days=-30)
                        ).count()
                        > 50
                    ):
                        # 오류가 발생해도 보낸 것중에서는 다시 보내지 않는다.
                        # 30일 이내에 50 건 이상이면 보내지 않는다.
                        target_date = invoice.bill.start_date
                        target_date = target_date.strftime("%Y년 %m월")
                        content = f"<송도비취타운> {target_date} 이용분 전기료 및 관리비가 미납되었습니다."
                        phone_number = invoice.contract.customer.phone
                        if phone_number:
                            send_sms(phone_number, content)
                            SMS(
                                content=content, invoice=invoice, to=phone_number
                            ).save()
                            sent_lst.append(phone_number)
            if sent_lst:
                send_sms("01044768444", f"{len(sent_lst)}건 관리비미납 SMS발송완료")
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
    scheduler.add_job(
        check_unbilled,
        "cron",
        day="13",
        hour="9",
        id="billing",
    )
    scheduler.start()
