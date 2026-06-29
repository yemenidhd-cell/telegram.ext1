import pyaudio
import wave
import os
from telegram import Update
from telegram.ext import ContextTypes

async def record_mic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("🎤 جاري التسجيل...")
    try:
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        record_seconds = 5

        p = pyaudio.PyAudio()
        stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
        frames = []
        for _ in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open("recording.wav", 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        await context.bot.send_audio(
            chat_id=user.id,
            audio=open("recording.wav", 'rb'),
            caption="🎤 تم التسجيل."
        )
        os.remove("recording.wav")
    except:
        await update.message.reply_text("❌ فشل التسجيل.")