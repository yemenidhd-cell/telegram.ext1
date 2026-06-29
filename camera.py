import cv2
import os
from telegram import Update
from telegram.ext import ContextTypes

async def capture_camera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("📸 جاري التقاط الصورة...")
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("capture.jpg", frame)
            cap.release()
            await context.bot.send_photo(
                chat_id=user.id,
                photo=open("capture.jpg", 'rb'),
                caption="📸 تم التقاط الصورة."
            )
            os.remove("capture.jpg")
        else:
            await update.message.reply_text("❌ فشل التقاط الصورة.")
    except:
        await update.message.reply_text("❌ لا توجد كاميرا متصلة.")