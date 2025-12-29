from celery import shared_task
import requests
from django.conf import settings

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 10}
)
def send_telegram_notification(
    self,
    order_id,
    product_name,
    quantity,
    customer_username,
    phone_number
):
    message = (
        f"🛒 <b>Yangi buyurtma</b>\n\n"
        f"🆔 Buyurtma ID: {order_id}\n"
        f"📦 Mahsulot: {product_name}\n"
        f"🔢 Soni: {quantity}\n"
        f"👤 Mijoz: {customer_username}\n"
        f"📞 Tel: {phone_number}"
    )

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": settings.TELEGRAM_ADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    return "Telegram notification sent"
