import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Order

@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if not created:
        return

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_ADMIN_CHAT_ID

    total_price = instance.product.price * instance.quantity

    message_text = (
        "<b>🛒 YANGI BUYURTMA!</b>\n"
        "━━━━━━━━━━━━━━━\n"
        f"<b>🆔 Buyurtma ID:</b> {instance.id}\n"
        f"<b>📦 Mahsulot:</b> {instance.product.name}\n"
        f"<b>🔢 Miqdor:</b> {instance.quantity}\n"
        f"<b>💰 Umumiy narx:</b> {total_price} so‘m\n"
        f"<b>📞 Telefon:</b> {instance.phone_number}\n"
        "━━━━━━━━━━━━━━━\n"
        "⏰ <i>Yangi buyurtma qabul qilindi</i>"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(
            url,
            json={"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"},
            timeout=5
        )
    except requests.RequestException as e:
        print(f"errors {e}")

