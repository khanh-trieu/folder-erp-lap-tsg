import datetime
import hashlib
import random
from calendar import SATURDAY, SUNDAY
from django.utils import timezone


class Timer(object):
    @classmethod
    def get_timestamp_now(cls):
        now = timezone.now()
        return int(datetime.datetime.timestamp(now))

    @classmethod
    def get_today(cls):
        now = timezone.now()
        return now.date()

    @classmethod
    def is_weekend(cls):
        weekend = timezone.now().weekday()
        if weekend == SATURDAY or weekend == SUNDAY:
            return True
        else:
            return False

    @classmethod
    def get_hour(cls):
        return timezone.now().hour

    @classmethod
    def get_current_month(cls):
        return timezone.now().month

    @classmethod
    def get_current_year(cls):
        return timezone.now().year

    @classmethod
    def get_timestamp(cls,timedate):
        date = datetime.datetime.strptime(timedate, "%Y/%m/%d")
        at = datetime.datetime.timestamp(date)
        return int(at)

def Convert_timestamp(timestamp):
    try:
        ts = datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y")
    except Exception as e:
        return ''
    return ts

def genpwd(leng):
    stringcode = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return (''.join(random.choice(stringcode) for i in range(leng)))

def encryption(text):
    result = hashlib.sha1(text.encode()).hexdigest()
    return result