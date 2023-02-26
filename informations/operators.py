from django.utils import timezone
from django.conf import settings
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from informations.models import Customer, Billing

logger = logging.getLogger(__name__)


def my_job():
    url = "https://opm.kepco.co.kr:11080/OpenAPI/getCustBillData"
    data_month = timezone.now().date().strftime("%Y%m")
    for cust in Customer.objects.all():
        params = {
            "custNo": cust.custNum,
            "serviceKey": settings.POWER_KEY,
            "dataMonth": data_month,
            "returnType": "JSON",
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            res = res.json()
            try:
                billing = res.get("custBillDataInfoList").get("custBillDataInfo")
                if not Billing.objects.filter(
                    bill_ym=billing.bill_ym, custNo=billing.custNo
                ).exists():
                    Billing.save(**billing)
            except:
                pass


def start():
    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="20", hour="09", minute="00"),
            id="my_job",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_a'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()  # 없으면 동작하지 않습니다.
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
