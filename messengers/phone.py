from django.conf import settings
from django.utils import timezone
import hashlib, hmac, base64, json, requests


def make_signature(urn, access_key, timestamp):

    # 환경변수
    secret_key = settings.SMS_SECRET_KEY
    secret_key = bytes(secret_key, "UTF-8")

    method = "POST"
    message = method + " " + urn + "\n" + timestamp + "\n" + access_key
    message = bytes(message, "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    )
    return signingKey


def send_sms(phone_number, content):

    # 환경변수
    access_key = settings.SMS_ACCESS_KEY
    urn = f"/sms/v2/services/{settings.SMS_SERVICE_ID}/messages"
    url = f"https://sens.apigw.ntruss.com{urn}"

    timestamp = f"{int(timezone.localtime(timezone.now()).timestamp()*1000)}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": make_signature(urn, access_key, timestamp),
    }

    message = {"to": phone_number}

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "024240187",
        "content": content,
        "messages": [message],
    }

    json_body = json.dumps(body)
    try:
        res = requests.post(url, headers=headers, data=json_body)
        res.raise_for_status()
    except:
        pass
