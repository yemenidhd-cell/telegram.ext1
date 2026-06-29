#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – وحدة استغلال تيك توك (معدلة لتجنب التعارض)

import requests
import json
import re

# تم تغيير اسم الكلاس
class TikTokExploitUtils:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.tiktok.com"

    def get_user_info(self, username):
        try:
            url = f"https://www.tiktok.com/api/v1/user/detail/?unique_id={username}"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "username": data.get("userInfo", {}).get("user", {}).get("uniqueId"),
                    "nickname": data.get("userInfo", {}).get("user", {}).get("nickname"),
                    "bio": data.get("userInfo", {}).get("user", {}).get("bioDescription"),
                    "followers": data.get("userInfo", {}).get("stats", {}).get("followerCount"),
                    "following": data.get("userInfo", {}).get("stats", {}).get("followingCount"),
                    "likes": data.get("userInfo", {}).get("stats", {}).get("heartCount"),
                    "videos": data.get("userInfo", {}).get("stats", {}).get("videoCount"),
                    "avatar": data.get("userInfo", {}).get("user", {}).get("avatarMedium")
                }
            return {"error": "المستخدم غير موجود"}
        except Exception as e:
            return {"error": str(e)}

    def get_user_videos(self, username, limit=10):
        try:
            url = f"https://www.tiktok.com/api/v1/user/posts/?unique_id={username}&count={limit}"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                videos = []
                for item in data.get("items", [])[:limit]:
                    videos.append({
                        "id": item.get("id"),
                        "desc": item.get("desc"),
                        "likes": item.get("stats", {}).get("diggCount"),
                        "shares": item.get("stats", {}).get("shareCount"),
                        "url": f"https://www.tiktok.com/@{username}/video/{item.get('id')}"
                    })
                return videos
            return []
        except:
            return []

# دالة للاستخدام المباشر في البوت (تم تغيير الاسم)
async def tiktok_exploit_utils(update, context):
    user = update.effective_user
    await update.message.reply_text(
        "🎵 **استغلال TikTok**\n\n"
        "📌 يتم جمع معلومات الحساب عبر API.\n"
        "⚠️ هذه الخدمة قيد التطوير.",
        parse_mode="Markdown"
    )
