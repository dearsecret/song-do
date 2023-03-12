from datetime import datetime
from dateutil.relativedelta import relativedelta


def count_month(start: datetime, end: datetime):
    # 두날짜 사이에 몇달인지 계산
    # 계약일자 28일 초과시 조정
    if start.day > 28:
        start = start.replace(day=28)
        end = end.replace(day=28)
    n = 0
    while end > start:
        start += relativedelta(months=1)
        n += 1
    return n
